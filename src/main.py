from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import set_webhook
from aiohttp import web
import logging
import os
import json
import mono
import limits
import scheduler


BOT_TOKEN = os.getenv('BOT_TOKEN')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f"https://{HEROKU_APP_NAME}.herokuapp.com"
BOT_WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
BOT_WEBHOOK_URL = f"{WEBHOOK_HOST}{BOT_WEBHOOK_PATH}"
MONO_WEBHOOK_PATH = f"/mono/{mono.MONO_TOKEN}"
MONO_WEBHOOK_URL = f"{WEBHOOK_HOST}{MONO_WEBHOOK_PATH}"


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Куку")
    try:
        mono.mono.create_webhook(MONO_WEBHOOK_URL)
    except Exception:
        print('error')


@dp.message_handler(commands=['limit'])
async def cmd_limit(message: types.Message):
    try:
        limit = message.text.split()[1]
        limits.set_limit(limit)
        await message.reply(f"Лимит установлен!\n"
                            f"Ваш лимит: {limit} грн")
    except IndexError:
        print('Не хватает аргументов')


@dp.message_handler(commands=['autolimit'])
async def cmd_autolimit(message: types.Message):
    try:
        balance = mono.get_balance()
        limit = limits.autolimit(balance)

        await message.reply(f"Лимит установлен!\n"
                            f"Ваш лимит: {limit} грн")

    except Exception:
        print("Ашибка")


async def on_startup(dispatcher):
    await bot.set_webhook(BOT_WEBHOOK_URL, drop_pending_updates=True)
    await scheduler.on_startup()
    limits.autolimit(mono.get_balance())


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
                limit = limits.get_limit()
                if amount < 0:
                    limit = limit - (amount * -1)
                    print(limit)

                await bot.send_message(chat_id=389471081, text=f"------------ Выписка ------------\n\n"
                                                               f"Описание: {description}\n"
                                                               f"Сумма: {int(amount)} грн\n"
                                                               f"Баланс: {balance} грн\n"
                                                               f"Лимит: {limit} грн")
        except json.decoder.JSONDecodeError:
            print('No POST data')

    else:
        print('just get request')

    return web.json_response({"status": "OK"}, status=200)


app = web.Application()
app.add_routes([web.route('*', MONO_WEBHOOK_PATH, monobank)])


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

