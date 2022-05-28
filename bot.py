import os
import telebot
from pathlib import Path
import config
from create_directory import create_directory
from shift_time_subtitle import *
import resources as R
from resources import MESSAGES

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
def file(message):
    bot.send_message(message.chat.id, MESSAGES['FILE'])


@bot.message_handler(content_types=['document'])
def get_file(message):
    """
    Prepares file for
    :param message:
    :return:
    """
    try:

        input_file_link = bot.get_file(message.document.file_id)
        input_files[message.chat.id] = [input_file_link, message.document.file_name]

        src_dir = create_directory(input_files[message.chat.id][1])
        # src_file_name = message.document.file_name

        os.chdir(src_dir)
        src_file = Path(input_files[message.chat.id][1])
        # src_file.write_bytes(file_content)
        src_file = str(Path(src_file).resolve())

        bot.reply_to(message, MESSAGES['TIME_DELTA'])
        bot.register_next_step_handler(message, get_new_file, src_file)
        # return to parent directory
        os.chdir(Path.cwd().parent)
    except Exception as e:
        bot.reply_to(message, e)


# @bot.message_handler()
@bot.message_handler(content_types=["text"])
def get_new_file(time_delta_message, src_file_name):
    try:
        new_file = shift_time_subtitle(src_file_name, int(time_delta_message.text))
        bot.reply_to(time_delta_message, MESSAGES['RUNNING_CONFIRM'].format(time_delta=time_delta_message.text))
        bot.send_document(time_delta_message.chat.id, document=open(new_file, 'rb'))
        file_content = bot.download_file(input_files[time_delta_message.chat.id][0].file_path)
        print(f"{file_content}")
    except Exception as e:
        print(e)


bot.polling(none_stop=True)
