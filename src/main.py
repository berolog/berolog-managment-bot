import monobank
import logging
import os
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.webhook import SendMessage
from aiogram import Bot, types
from flask import Flask, request, abort


app = Flask(__name__)


MONO_TOKEN = os.getenv('MONO_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

mono = monobank.Client(MONO_TOKEN)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
#    return SendMessage(chat_id=message.chat.id, text='Hi from webhook!',
#                       reply_to_message_id=message.message_id)
#    await bot.get_webhook_info()


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


@app.route('/' + WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.method == 'POST':
        ##if request.json['data']['account'] == '7dxOnvxACiayZfZzNvs6fA':
        print(request.json)
        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host=WEBAPP_HOST, port=WEBAPP_PORT)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

    mono.create_webhook(WEBHOOK_URL)
