import monobank
import json
import logging
from aiogram import Bot, Dispatcher, executor, types
from datetime import date
from buttons import inline_keyboard


bot_token = '5162165790:AAHD_2v5tB5hntJY9S0Gy-mtnAIrFc--uSg'
mono_token = 'u8PI0F5SA36yJrCPaWamBEGsTFjyrZWdkyRbIgYf_Ltk'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

mono = monobank.Client(mono_token)
mono.create_webhook('https://smee.io/84Q5y92SZExUCbe')
user_info = mono.get_client_info()
statements = mono.get_statements(account=user_info['accounts'][1]['id'], date_from=date.today())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
#    butt_info = [{'text': "Установить лимит", 'callback': "setlimit"}]
#    keyboard = inline_keyboard(butt_info)

#    await message.reply(f"Имя: {user_info['name']}\n"
#                        f"Баланс: {user_info['accounts'][1]['balance']/100}",
#                        reply_markup=keyboard)

#    await message.reply(f"Выписки: {statements}")
#    keyboard = types.ReplyKeyboardMarkup()
#    data = types.KeyboardButton(text='Лимит')
#    keyboard.add(data)

    await message.reply('Ураа')

#@dp.message_handler()
#async def echo(message: types.Message):
#    if message.text == "Лимит":
#        await message.answer("Срака")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

