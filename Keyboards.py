from telebot import types
from googletrans import LANGCODES


def start_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton(text="Start"),
        types.KeyboardButton(text="History")
    )
    return markup


def lang_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = []
    for lang in LANGCODES.keys():
        button = types.KeyboardButton(text=lang.title())
        buttons.append(button)
    markup.add(*buttons)
    return markup


