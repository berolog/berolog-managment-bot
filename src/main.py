from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.webhook import configure_app
from aiogram.utils.executor import set_webhook
from aiohttp import web
import logging
import os
import monobank
import json


BOT_TOKEN = os.getenv('BOT_TOKEN')
MONO_TOKEN = os.getenv('MONO_TOKEN')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f"https://{HEROKU_APP_NAME}.herokuapp.com"
BOT_WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
BOT_WEBHOOK_URL = f"{WEBHOOK_HOST}{BOT_WEBHOOK_PATH}"
MONO_WEBHOOK_PATH = f"/mono/{MONO_TOKEN}"
MONO_WEBHOOK_URL = f"{WEBHOOK_HOST}{MONO_WEBHOOK_PATH}"

mono = monobank.Client(MONO_TOKEN)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await mono.create_webhook(MONO_WEBHOOK_URL)


async def on_startup(dispatcher):
    await bot.set_webhook(BOT_WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


async def monobank(request):
    if request.method == 'POST':
        try:
            data = await request.json()
            account = data['data']['account']
            if account == os.getenv('MONO_ACCOUNT'):
                description = data['data']['statementItem']['description']
                amount = data['data']['statementItem']['amount']/100
                balance = data['data']['statementItem']['balance']/100

                await bot.send_message(chat_id=389471081, text=f"------------ Выписка ------------\n\n"
                                                               f"Описание: {description}\n"
                                                               f"Сумма: {int(amount)} грн\n"
                                                               f"Баланс: {balance} грн")
        except json.decoder.JSONDecodeError:
            print('No POST data')

    else:
        print('just get request')

    return web.json_response({"status": "OK"}, status=200)


app = web.Application()
app.add_routes([web.route('*', MONO_WEBHOOK_PATH, monobank)])
#configure_app(dp, app, BOT_WEBHOOK_PATH)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    executor = set_webhook(dispatcher=dp,
                           webhook_path=BOT_WEBHOOK_PATH,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           route_name='bot',
                           web_app=app)
    executor.run_app(host='0.0.0.0', port=os.getenv('PORT', 9000))

