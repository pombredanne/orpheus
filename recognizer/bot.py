# # -*- coding: utf-8 -*-

import os
import time
import telegram

from telegram.ext import Updater

import search
import config as cf


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    try:
        time_begin = time.time()
        file_name = update.message.voice.file_id + '.ogg'
        newFile = bot.getFile(update.message.voice.file_id)
        newFile.download('voices/{}'.format(file_name))

        tracks = search.SearchApp().run(file_name, cf.FOLDER_BOT)
        bot.sendMessage(chat_id=update.message.chat_id, text='Processing time = ' + str(time.time() - time_begin))
        bot.sendMessage(chat_id=update.message.chat_id, text='\n'.join(tracks))

        bot.sendPhoto(chat_id=update.message.chat_id, photo=open(os.path.join(cf.FOLDER_TEMP, 'foo.png'), 'rb'))

    except Exception as e:
        print(e)


token = '217941149:AAEXCQ1BSKwPrFxJjpebolwoMoDIsS-ZTlM'
bot = telegram.Bot(token=token)
updater = Updater(token=token)

dispatcher = updater.dispatcher
dispatcher.addTelegramCommandHandler('start', start)

updater.start_polling()

dispatcher.addTelegramMessageHandler(echo)
