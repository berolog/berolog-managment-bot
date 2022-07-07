import monobank
import logging
import os
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.webhook import SendMessage
from aiogram.dispatcher.webhook import configure_app, WebhookRequestHandler
from aiogram import Bot, types
from aiohttp import web


MONO_TOKEN = os.getenv('MONO_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

app = web.Application()
app.router.add_route('*', WEBHOOK_PATH, WebhookRequestHandler, name='webhook_handler')

mono = monobank.Client(MONO_TOKEN)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
app['BOT_DISPATCHER'] = dp


@dp.message_handler()
async def echo(message: types.Message):
    return SendMessage(chat_id=message.chat.id, text='Hi from webhook!',
                       reply_to_message_id=message.message_id)
#    await bot.get_webhook_info()


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        app=app
    )

    mono.create_webhook(WEBHOOK_URL)
