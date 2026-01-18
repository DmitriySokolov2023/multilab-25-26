# main.py
import os
import logging
import asyncio
from pathlib import Path

import aiohttp
from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.constants import ParseMode, ChatAction
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

# ----------------- STATES -----------------
ASK_NAME, ASK_AGE = range(2)

# ----------------- BUTTONS -----------------
BTN_MENU = "🍔 Меню"            # можно оставить просто "Меню", но так нагляднее
BTN_HELP = "ℹ️ Помощь"
BTN_HIDE = "🙈 Скрыть клавиатуру"

MAIN_KB = ReplyKeyboardMarkup(
    [
        [BTN_MENU, BTN_HELP],
        [BTN_HIDE],
    ],
    resize_keyboard=True,
)

def build_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🐱 Факт о котах", callback_data="menu:cat")],
            [InlineKeyboardButton("🐶 Фото собаки", callback_data="menu:dog")],
            [InlineKeyboardButton("👤 Заполнить профиль", callback_data="menu:profile")],
            [InlineKeyboardButton("🔢 Счётчик", callback_data="menu:count")],
            [InlineKeyboardButton("❓ Помощь", callback_data="menu:help")],
            [InlineKeyboardButton("❌ Закрыть меню", callback_data="menu:close")],
        ]
    )

def get_active_message(update: Update):
    """Чтобы отвечать и при /команде, и при callback."""
    if update.message:
        return update.message
    if update.callback_query and update.callback_query.message:
        return update.callback_query.message
    return None

# ----------------- CONFIG -----------------
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("В .env не найден BOT_TOKEN.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("ptb-intro")

# ----------------- COMMON ACTIONS -----------------
async def do_help(message, context: ContextTypes.DEFAULT_TYPE):
    await message.reply_text(
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/help — помощь\n"
        "/menu — меню\n"
        "/sum a b — сложить два числа\n"
        "/count — твой счётчик\n"
        "/cat — факт о котиках (async)\n"
        "/dog — фото собаки (async)\n"
        "/profile — анкета (имя/возраст)\n"
        "/cancel — отменить диалог\n\n"
        "Также можно пользоваться кнопками 👇",
        reply_markup=MAIN_KB,
    )

async def do_count(message, context: ContextTypes.DEFAULT_TYPE):
    cnt = context.user_data.get("count", 0) + 1
    context.user_data["count"] = cnt
    await message.reply_text(f"Ты вызывал(а) счётчик {cnt} раз(а).", reply_markup=MAIN_KB)

async def do_cat(message, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=message.chat_id, action=ChatAction.TYPING)
    await asyncio.sleep(0.2)

    url = "https://catfact.ninja/fact"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.json()

        fact = data.get("fact") or "Не нашёл факт 😿"
        await message.reply_text(f"🐱 {fact}", reply_markup=MAIN_KB)
    except Exception:
        logger.exception("Ошибка получения факта о котах")
        await message.reply_text("Не удалось получить факт. Попробуй позже.", reply_markup=MAIN_KB)

async def do_dog(message, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    await asyncio.sleep(0.2)

    url = "https://dog.ceo/api/breeds/image/random"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.json()

        photo_url = data.get("message")
        if not photo_url:
            await message.reply_text("Не удалось получить фото 🐾", reply_markup=MAIN_KB)
            return

        await message.reply_photo(photo=photo_url, caption="🐶 Держи собаку!", reply_markup=MAIN_KB)
    except Exception:
        logger.exception("Ошибка получения фото собаки")
        await message.reply_text("Не удалось загрузить фото 🐾", reply_markup=MAIN_KB)

# ----------------- COMMANDS -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я учебный бот.\n"
        "Нажми 🍔 Меню или используй команды: /help, /sum, /count, /cat, /dog, /profile.\n"
        "Напиши текст — повторю его.",
        reply_markup=MAIN_KB,
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_help(update.message, context)

async def sum_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Использование: /sum 2 3")
        return
    try:
        a, b = map(int, context.args)
    except ValueError:
        await update.message.reply_text("Аргументы должны быть целыми числами: /sum 2 3")
        return
    await update.message.reply_text(
        f"{a} + {b} = <b>{a + b}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=MAIN_KB,
    )

async def count_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_count(update.message, context)

async def cat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_cat(update.message, context)

async def dog_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_dog(update.message, context)

# ----------------- MENU -----------------
async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Меню 👇", reply_markup=build_menu_inline())

async def menu_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Меню 👇", reply_markup=build_menu_inline())

async def menu_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data.split(":", 1)[1]
    message = query.message

    if action == "cat":
        await do_cat(message, context)
    elif action == "dog":
        await do_dog(message, context)
    elif action == "count":
        await do_count(message, context)
    elif action == "help":
        await do_help(message, context)
    elif action == "close":
        try:
            await message.edit_text(f"Меню закрыто ✅\nНажми «{BTN_MENU}», чтобы открыть снова.")
        except Exception:
            await message.reply_text("Меню закрыто ✅", reply_markup=MAIN_KB)

# ----------------- TEXT BUTTONS -----------------
async def help_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await do_help(update.message, context)

async def hide_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Клавиатура скрыта 🙈", reply_markup=ReplyKeyboardRemove())

# ----------------- ECHO -----------------
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Эхо: {update.message.text}", reply_markup=MAIN_KB)

# ----------------- PROFILE CONVERSATION -----------------
async def profile_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # поддержка запуска и командой, и из inline-меню
    if update.callback_query:
        await update.callback_query.answer()

    message = get_active_message(update)
    if message is None:
        return ConversationHandler.END

    prof = context.user_data.get("profile")

    # Если профиль уже есть — показать и выйти
    if isinstance(prof, dict) and "name" in prof and "age" in prof:
        await message.reply_text(
            f"Твой профиль:\n<b>{prof['name']}</b>\nВозраст: <b>{prof['age']}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=MAIN_KB,
        )
        return ConversationHandler.END

    # Иначе начать диалог
    await message.reply_text("Как тебя зовут?", reply_markup=ReplyKeyboardRemove())
    return ASK_NAME

async def profile_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = (update.message.text or "").strip()
    if len(name) < 2:
        await update.message.reply_text("Имя слишком короткое. Введи снова:")
        return ASK_NAME

    context.user_data.setdefault("profile", {})["name"] = name
    await update.message.reply_text("Сколько тебе лет? (числом)")
    return ASK_AGE

async def profile_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (update.message.text or "").strip()
    if not txt.isdigit():
        await update.message.reply_text("Нужно число. Введи возраст:")
        return ASK_AGE

    age = int(txt)
    if not (1 <= age <= 120):
        await update.message.reply_text("Возраст 1..120. Попробуй снова:")
        return ASK_AGE

    context.user_data.setdefault("profile", {})["age"] = age
    prof = context.user_data["profile"]

    await update.message.reply_text(
        f"Готово!\nИмя: <b>{prof['name']}</b>\nВозраст: <b>{prof['age']}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=MAIN_KB,
    )
    return ConversationHandler.END

async def profile_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог отменён.", reply_markup=MAIN_KB)
    return ConversationHandler.END

conv = ConversationHandler(
    entry_points=[
        CommandHandler("profile", profile_start),
        CallbackQueryHandler(profile_start, pattern=r"^menu:profile$"),
    ],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_name)],
        ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_age)],
    },
    fallbacks=[CommandHandler("cancel", profile_cancel)],
    name="profile_conv",
    persistent=True,
)

# ----------------- ERROR -----------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception("Unhandled exception", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Ой! Случилась ошибка. Уже чиним 🤖",
            reply_markup=MAIN_KB,
        )

# ----------------- MAIN -----------------
def main():
    base_dir = Path(__file__).resolve().parent
    pkl_path = base_dir / "bot_data.pkl"

    persistence = PicklePersistence(filepath=str(pkl_path))

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .persistence(persistence)
        .build()
    )

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("menu", menu_cmd))
    app.add_handler(CommandHandler("sum", sum_cmd))
    app.add_handler(CommandHandler("count", count_cmd))
    app.add_handler(CommandHandler("cat", cat_cmd))
    app.add_handler(CommandHandler("dog", dog_cmd))

    # Текстовые кнопки снизу
    app.add_handler(MessageHandler(filters.Regex(f"^{BTN_MENU}$"), menu_text))
    app.add_handler(MessageHandler(filters.Regex(f"^{BTN_HELP}$"), help_text))
    app.add_handler(MessageHandler(filters.Regex(f"^{BTN_HIDE}$"), hide_keyboard))

    # Анкета (важно добавить ДО общего callback меню)
    app.add_handler(conv)

    # Inline-меню (кроме profile — его ловит ConversationHandler выше)
    app.add_handler(CallbackQueryHandler(menu_cb, pattern=r"^menu:(cat|dog|count|help|close)$"))

    # Эхо — всегда последним
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
