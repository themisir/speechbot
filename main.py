#!/usr/bin/env python3

import os
import logging

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from transcriber import Transcriber

import utils

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

transcriber = Transcriber()
logger = logging.getLogger(__name__)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"[{update.message.message_id}] Transcribing voice message. "
                f"User: {update.message.from_user.username} (#{update.message.from_user.id}); "
                f"Chat: #{update.message.chat.id}")

    oga_path = utils.temp_file(suffix='.oga')
    try:
        file = await update.message.voice.get_file()
        await file.download_to_drive(oga_path)
        transcript = transcriber.process_file(oga_path)
        logger.info(f"[{update.message.message_id}] Transcript: {transcript}")
        await context.bot.send_message(text=f'{transcript}',
                                       chat_id=update.message.chat_id,
                                       reply_to_message_id=update.message.message_id)
    except Exception as e:
        logger.error(f"[{update.message.message_id}] Error: {e}")
    finally:
        os.unlink(oga_path)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()
    application.add_handler(MessageHandler(filters.VOICE, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
