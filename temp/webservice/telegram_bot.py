from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Servidores
import io
import datetime
token = '650314066:AAFrittaRz9-P_rcBHGmy7jpzYsOVIueVeU'
request_kwargs = {
    'proxy_url': 'http://f3012012:f3012012@10.50.1.3:8080/',
}
updater = Updater(token=token, request_kwargs=request_kwargs)
dispatcher = updater.dispatcher

class FilterServidor(BaseFilter):
    def filter(self, message):
        return 'produtividade do servidor' in message.text

filter_servidor = FilterServidor()


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Para relatorio de produtividade atual diga "atual"')

def prodServ(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)



servidor_handler = MessageHandler(filter_servidor, prodServ)
dispatcher.add_handler(servidor_handler)
dispatcher.add_handler(CommandHandler("start", start))

updater.start_polling()
