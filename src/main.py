from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.webhook import configure_app
from aiohttp import web
import os
import monobank

MONO_TOKEN = os.getenv('MONO_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')

mono = monobank.Client(MONO_TOKEN)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("start!")


# handle /api route
async def api_handler(request):
    print(web.json_response)
    return web.json_response({"status": "OK"}, status=200)


app = web.Application()
# add a custom route
app.add_routes([web.post('/api', api_handler)])
# every request to /bot route will be retransmitted to dispatcher to be handled
# as a bot update
configure_app(dp, app, "/bot")

if __name__ == '__main__':
    web.run_app(app, port=os.getenv('PORT', 9000))
    mono.create_webhook('https://berolog-managment-bot.herokuapp.com/api')
