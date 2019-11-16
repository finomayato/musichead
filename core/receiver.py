import os
import logging

from telegram import MessageEntity
from telegram.ext import Updater, MessageHandler, Filters, BaseFilter

from core.youtube import is_youtube_link, YouTubeConverter
from core.spotify import is_spotify_link, SpotifyConverter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

DefaultFilter = Filters.text & (Filters.entity(MessageEntity.URL) | Filters.entity(MessageEntity.TEXT_LINK))


def _get_message_processor(receiver_converter, converters):
    def processor(update, context):
        for converter in converters:
            new_link = converter.get_link(receiver_converter.get_title(update.message.text))
            context.bot.send_message(chat_id=update.effective_chat.id, text=new_link)
    return processor


def _get_custom_filter(filter_expression):
    class CustomFilter(BaseFilter):
        def filter(self, message):
            return filter_expression(message.text)

    return CustomFilter()


def _add_link_hanlders(dispatcher):
    youtube_converter = YouTubeConverter()
    spotify_converter = SpotifyConverter()
    handlers = [
        (is_youtube_link, youtube_converter, [spotify_converter]),
        (is_spotify_link, spotify_converter, [youtube_converter])
    ]
    for handler in handlers:
        dispatcher.add_handler(
            MessageHandler(DefaultFilter & _get_custom_filter(handler[0]),
                           _get_message_processor(handler[1], handler[2]))
        )


if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    _add_link_hanlders(dispatcher)

    updater.start_polling()
