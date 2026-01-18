import os
import time
import asyncio
import logging

from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    PicklePersistence,
    filters,
)

import aiohttp

# ================== НАСТРОЙКА ==================

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("В .env не найден BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("ptb-v2")

# ================== КЛАВИАТУРЫ ==================

MAIN_KB = ReplyKeyboardMarkup(
    [
        ["/cat", "/dog"],
        ["/profile", "/count"],
        ["/help"]
    ],
    resize_keyboard=True
)

# ================== АНТИСПАМ ==================

THROTTLE_SECONDS = 2.0
_last_call: dict[int, float] = {}


def is_throttled(user_id: int) -> bool:
    now = time.time()
    last = _last_call.get(user_id, 0)
    if now - last < THROTTLE_SECONDS:
        return True
    _last_call[user_id] = now
    return False


# ================== ХЕНДЛЕРЫ ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\n"
        "Я учебный Telegram-бот.\n\n"
        "Основные команды:\n"
        "/cat — факт о котах\n"
        "/dog — фото собаки\n"
        "/profile — анкета\n"
        "/count — счётчик\n",
        reply_markup=MAIN_KB
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Команды:\n"
        "/start — старт\n"
        "/menu — меню\n"
        "/cat — факт о коте\n"
        "/dog — фото собаки\n"
        "/profile — заполнить профиль\n"
        "/count — счётчик вызовов\n"
        "\nЯ также повторяю любой текст 🙂",
        reply_markup=MAIN_KB
    )


async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Меню 👇", reply_markup=MAIN_KB)


async def count_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = context.user_data.get("count", 0) + 1
    context.user_data["count"] = count
    await update.message.reply_text(f"Ты вызывал(а) /count {count} раз(а).")


# ================== CAT ==================

async def cat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_throttled(user_id):
        await update.message.reply_text("Слишком часто 😅 Подожди пару секунд.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    url = "https://catfact.ninja/fact"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.json()

        fact = data.get("fact", "Факт не найден 😿")
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Ещё факт 🐱", callback_data="cat_more")]]
        )

        await update.message.reply_text(f"🐱 {fact}", reply_markup=keyboard)

    except Exception:
        logger.exception("Ошибка /cat")
        await update.message.reply_text("Не удалось получить факт 😿")


async def cat_more_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if is_throttled(user_id):
        await query.message.reply_text("Подожди немного ⏳")
        return

    url = "https://catfact.ninja/fact"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.json()

        await query.message.reply_text(f"🐱 {data.get('fact')}")

    except Exception:
        logger.exception("Ошибка cat_more")
        await query.message.reply_text("Ошибка при получении факта 😿")


# ================== DOG ==================

async def dog_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_throttled(user_id):
        await update.message.reply_text("Слишком часто 😅")
        return

    await context.bot.send_chat_action(
        update.effective_chat.id,
        ChatAction.UPLOAD_PHOTO
    )

    url = "https://dog.ceo/api/breeds/image/random"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.json()

        await update.message.reply_photo(
            photo=data.get("message"),
            caption="🐶 Случайная собака",
            reply_markup=MAIN_KB
        )

    except Exception:
        logger.exception("Ошибка /dog")
        await update.message.reply_text("Не удалось загрузить фото 🐾")


# ================== PROFILE (DIALOG) ==================

ASK_NAME, ASK_AGE = range(2)


async def profile_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Как тебя зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    return ASK_NAME


async def profile_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if len(name) < 2:
        await update.message.reply_text("Имя слишком короткое, попробуй ещё раз:")
        return ASK_NAME

    context.user_data.setdefault("profile", {})["name"] = name
    await update.message.reply_text("Сколько тебе лет? (числом)")
    return ASK_AGE


async def profile_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.isdigit():
        await update.message.reply_text("Возраст должен быть числом:")
        return ASK_AGE

    age = int(text)
    context.user_data.setdefault("profile", {})["age"] = age
    profile = context.user_data["profile"]

    await update.message.reply_text(
        f"Профиль сохранён ✅\n\n"
        f"Имя: <b>{profile['name']}</b>\n"
        f"Возраст: <b>{profile['age']}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=MAIN_KB
    )
    return ConversationHandler.END


async def profile_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Анкета отменена.", reply_markup=MAIN_KB)
    return ConversationHandler.END


# ================== ЭХО ==================

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Эхо: {update.message.text}")


# ================== ERROR ==================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception("Unhandled exception", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Произошла ошибка 🤖 Мы уже разбираемся."
        )


# ================== MAIN ==================

def main():
    persistence = PicklePersistence(filepath="bot_data.pkl")

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .persistence(persistence)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("menu", menu_cmd))
    app.add_handler(CommandHandler("count", count_cmd))
    app.add_handler(CommandHandler("cat", cat_cmd))
    app.add_handler(CommandHandler("dog", dog_cmd))

    app.add_handler(CallbackQueryHandler(cat_more_cb, pattern="^cat_more$"))

    profile_conv = ConversationHandler(
        entry_points=[CommandHandler("profile", profile_start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_name)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_age)],
        },
        fallbacks=[CommandHandler("cancel", profile_cancel)],
        name="profile_conv",
        persistent=True,
    )
    app.add_handler(profile_conv)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)

    logger.info("Бот v2 запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
