# pytelegrambotapi
# python-dotenv

from dotenv import load_dotenv
from telebot import TeleBot, types
import os
import Keyboards as kb
from googletrans import Translator, LANGCODES
import database as db

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = TeleBot(token=TOKEN)
translator = Translator()


# @bot.message_handler(commands=['start', 'help'])
# def start(message: types.Message):
#     chat_id = message.chat.id
#     first_name = message.from_user.first_name
#     if message.text == '/start':
#         bot.send_message(chat_id, f'Привет, {first_name}')
#     elif message.text == '/help':
#         bot.send_message(chat_id, 'Помощь по боту')


# @bot.message_handler(content_types=['text'])
# def answer(message: types.Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, message.text)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    db.add_user(first_name, chat_id)
    bot.send_message(chat_id, 'Выберите действие снизу',
                     reply_markup=kb.start_kb())


@bot.message_handler(func=lambda msg: msg.text == "Start")
def start_translation(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык, с которого хотите сделать перевод',
                     reply_markup=kb.lang_menu())
    bot.register_next_step_handler(message, get_lang_from)


@bot.message_handler(func=lambda msg: msg.text == "History")
def get_history(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Ваша история переводов: ")
    bot.send_message(chat_id, db.get_history(chat_id))


def get_lang_from(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык, на который хотите сделать перевод',
                     reply_markup=kb.lang_menu())
    bot.register_next_step_handler(message, get_lang_to, message.text)


def get_lang_to(message: types.Message, lang_from):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напишите слово или текст для перевода',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, message.text)


def translate(message: types.Message, lang_from, lang_to):
    chat_id = message.chat.id
    _from = LANGCODES[lang_from.lower()]
    _to = LANGCODES[lang_to.lower()]
    translated_text = translator.translate(message.text, dest=_to, src=_from).text
    db.add_translation(_from, _to, message.text, translated_text, chat_id)
    bot.send_message(chat_id, translated_text)
    start(message)


bot.polling(none_stop=True)
