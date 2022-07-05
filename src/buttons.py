from aiogram import types


# Функция вывода инлайн кнопок
def inline_keyboard(butt_info):
    try:
        keyboard = types.InlineKeyboardMarkup()

        for i in range(len(butt_info)):
            keyboard_i = types.InlineKeyboardButton(text=butt_info[i]['text'],
                                                    callback_data=butt_info[i]['callback'])
            keyboard.add(keyboard_i)

        return keyboard

    except KeyError as key:
        print('Error in key')


# Функция вывода reply кнопок
def reply_keyboard(butt_info):
    try:
        keyboard = types.ReplyKeyboardMarkup()

        for i in range(len(butt_info)):
            keyboard_i = types.KeyboardButton(text=butt_info[i]['text'])
            keyboard.add(keyboard_i)

        return keyboard

    except KeyError as key:
        print('Error in key')