import telebot
from telegram_bot.config import TELEGRAM_BOT_TOKEN, HOST_ADDRESS
from telegram_bot.utils.lang import get_bot_message
from telegram_bot.utils.common_utils import get_random_string
from telegram_bot.utils.fast_api_client import get_text

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
HOST_ADDRESS = HOST_ADDRESS
DEFAULT_LANG = "EN"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send Welcome message

    Args:
        message : telebot object
    """
    answer = f'{get_bot_message(DEFAULT_LANG, "Welcome")}'
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['help'])
def help_info(message):
    """Help info for /help command

    Args:
        message : telebot object
    """
    answer = f'{get_bot_message(DEFAULT_LANG, "HelpInfo")}'
    bot.send_message(message.chat.id, answer)

@bot.message_handler(func=lambda message: True)
def message_processing(message):
    """Handler for message

    Args:
        message : telebot object
    """
    answer = f'{get_bot_message(DEFAULT_LANG, "Tips")}'
    bot.reply_to(message, answer)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    """Handler for Voice message. This function get Voice Message and next send it to FastAPI Server. 
    Recieve Text from ASR Service

    Args:
        message : telebot object
    """
    user = message.from_user.id
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    audio_file_name = f'telegram_bot/voice_messages/{user}_{get_random_string(3)}.ogg'
    with open(audio_file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    text = get_text(audio_file_name, HOST_ADDRESS)
    if text['text'] == '':
        answer = f'{get_bot_message(DEFAULT_LANG, "EmptyMessage")}'
        bot.reply_to(message, answer)
    else:
        bot.reply_to(message, text['text'])