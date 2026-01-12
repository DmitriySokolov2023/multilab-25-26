from asyncio.log import logger
import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("В .env не найден BOT_TOKEN.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("start")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот на Python.")
    
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/help — помощь\n"
        "/sum a b — сложить два числа\n"
        "/count — твой счётчик\n"
        "/cat — факт о котиках (async)\n"
        "И ещё я отвечаю эхом на обычный текст."
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    logger.info("Пустое приложение создано. Нажми Ctrl+C для выхода.")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.run_polling()

if __name__ == "__main__":
    main()