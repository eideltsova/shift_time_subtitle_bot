import os
import telebot
from pathlib import Path
import config
from create_directory import create_directory
from shift_time_subtitle import *
import resources as R
from resources import MESSAGES
import string

token = config.token
bot = telebot.TeleBot(token)

input_files = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, MESSAGES['START'])


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, MESSAGES['HELP'])


@bot.message_handler(commands=['file'])
def file_message(message):
    bot.send_message(message.chat.id, MESSAGES['FILE'])


@bot.message_handler(content_types=['document'])
def get_file(message):
    """
    Prepares file for modify
    :param message:
    :return:
    """
    try:
        input_file_link = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        src_dir = create_directory(file_name)
        os.chdir(src_dir)
        src_file = str(Path(file_name).resolve())
        input_files[message.chat.id] = [input_file_link, src_file]
        bot.reply_to(message, MESSAGES['TIME_DELTA'])
        bot.register_next_step_handler(message, set_time_delta)
        os.chdir(Path.cwd().parent)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=["text"])
def set_time_delta(message):
    try:
        time_delta = message.text
        if not time_delta.isdigit():
            bot.reply_to(message, MESSAGES["INCORRECT_TIME"])
            bot.register_next_step_handler(message, set_time_delta)
            return
        else:
            bot.reply_to(message, MESSAGES['RUNNING_CONFIRM'].format(time_delta=message.text))
            get_new_file(int(time_delta), message)
    except TypeError as e:
        bot.reply_to(message, e)


def get_new_file(time_delta: int, message) -> str:
    save_input_file(message)
    try:
        new_file = shift_time_subtitle(input_files.get(message.chat.id)[1], time_delta)
        input_files.get(message.chat.id).append(new_file)
        bot.send_document(message.chat.id, document=open(new_file, 'rb'))
        delete_input_file(input_files.get(message.chat.id)[1])
    except Exception as e:
        bot.reply_to(message, e)


def save_input_file(message: list) -> None:
    file_content = bot.download_file(input_files.get(message.chat.id)[0].file_path)
    Path(input_files.get(message.chat.id)[1]).write_bytes(file_content)


def delete_input_file(file_name: str):
    Path.unlink(Path(file_name), missing_ok=True)
    print("File was deleted")


bot.polling(none_stop=True)
