import logging
import os
from typing import Callable, List

from telegram import Message, MessageEntity
from telegram.ext import BaseFilter, Dispatcher, Filters, MessageHandler, Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from .common import FilterExpression, Service
from .spotify import Spotify
from .youtube import YouTube

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def _get_message_processor(receiver_service: Service, services: List[Service]) -> Callable[..., None]:
    def processor(update: Update, context: CallbackContext) -> None:
        log.info(f'Got "{update.message.text}"')
        for service in services:
            try:
                new_link = service.converter.get_link(
                    receiver_service.converter.get_track_metadata(update.message.text))
            except Exception:
                logging.exception(f'{update.message.text} was not converted to {service.name} link')
                new_link = (f"Sorry, I was unable to find a link in {service.name.capitalize()}. "
                            "But don't worry, I logged that issue, so it will be fixed soon!")
            else:
                log.info(f'Link "{update.message.text}" was converted to "{new_link}"')
            context.bot.send_message(chat_id=update.effective_chat.id, text=new_link)
    return processor


def _get_custom_filter(filter_expression: FilterExpression):  # type: ignore
    class CustomFilter(BaseFilter):  # type: ignore  # TODO: fix when telegram will be annotated
        def filter(self, message: Message) -> bool:
            return filter_expression(message.text)

    return CustomFilter()


class Handler:
    def __init__(self, dispatcher: Dispatcher, services: List[Service]) -> None:
        self.dispatcher = dispatcher
        self.services = services

    def add_handlers(self) -> None:
        for service in self.services:
            remaining_services = self.services.copy()
            remaining_services.remove(service)  # TODO: add more elegant solution

            self.dispatcher.add_handler(MessageHandler(
                self._filter(service.is_convertible_link), _get_message_processor(service, remaining_services))
            )

    def _filter(self, filter_expression: FilterExpression) -> bool:
        default_filter = Filters.text & (Filters.entity(MessageEntity.URL) | Filters.entity(MessageEntity.TEXT_LINK))
        custom_filter = _get_custom_filter(filter_expression)
        return default_filter & custom_filter


if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    services = [Spotify, YouTube]
    handler = Handler(dispatcher=updater.dispatcher, services=services)
    handler.add_handlers()

    updater.start_polling()
