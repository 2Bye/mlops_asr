# from uvicorn import run
# from fast_api_module.fast_api_server import app
from telegram_bot.app import run_bot
from loguru import logger


if __name__ == "__main__":
    logger.info("application start")
    run_bot()
    # run(app=app, log_level="debug", host="127.0.0.1", port=5454)