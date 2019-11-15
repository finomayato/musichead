import logging

from telegram import MessageEntity
from telegram.ext import Updater, MessageHandler, Filters

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TELEGRAM_BOT_TOKEN = '<>'

updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)


dispatcher = updater.dispatcher


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


echo_handler = MessageHandler(
    Filters.text & (Filters.entity(MessageEntity.URL) |
                    Filters.entity(MessageEntity.TEXT_LINK)),
    echo
)
dispatcher.add_handler(echo_handler)


updater.start_polling()
