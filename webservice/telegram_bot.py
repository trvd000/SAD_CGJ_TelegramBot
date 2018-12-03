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
    'proxy_url': 'http://f3012012:Trvd025665%35@10.50.1.3:8080/',
}
updater = Updater(token=token, request_kwargs=request_kwargs)
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Para relatorio de produtividade atual diga "atual"')

dispatcher.add_handler(CommandHandler("start", start))

updater.start_polling()
