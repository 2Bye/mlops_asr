from telegram_bot.bot import bot
from loguru import logger

def run_bot():
    logger.info("Bot start")
    bot.infinity_polling()