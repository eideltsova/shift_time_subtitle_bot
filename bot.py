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


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, R.START_MESSAGE)


@bot.message_handler(commands=['file'])
def file(message):
    bot.send_message(message.chat.id, "Please, choose file which you wanna change..")


@bot.message_handler(content_types=['document'])
def get_file(message):
    try:
        file = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file.file_path)
        src_dir = create_directory(message.document.file_name)
        src_file_name = message.document.file_name

        os.chdir(src_dir)
        src_file = Path(src_file_name)
        src_file.write_bytes(downloaded_file)
        src_file = Path(src_file).resolve()
        bot.reply_to(message, f"Please, input time delta. Time can be negative or positive. Time must be in a seconds")
        bot.register_next_step_handler(message, get_new_file, src_file)
        # return to parent directory
        os.chdir(Path.cwd().parent)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=["text"])
def get_new_file(time_delta_message, src_file_name):
    try:
        new_file = shift_time_subtitle(str(src_file_name), int(time_delta_message.text))
        bot.reply_to(time_delta_message, MESSAGES['RUNNING_CONFIRM'].format(time_delta=time_delta_message.text))
        bot.send_document(time_delta_message.chat.id, document=open(new_file, 'rb'))
    except Exception as e:
        print(e)



bot.polling(none_stop=True)
