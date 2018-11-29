from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Servidores
import io
import datetime


engine = create_engine('sqlite:///servidores.db')#, connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

updater = Updater(token='650314066:AAFrittaRz9-P_rcBHGmy7jpzYsOVIueVeU')
dispatcher = updater.dispatcher

class FilterAtual(BaseFilter):
    def filter(self, message):
        return 'atual' in message.text

class FilterThird(BaseFilter):
    def filter(self, message):
        return 'manda o terceiro' in message.text

filter_atual = FilterAtual()
filter_third = FilterThird()

def atual(bot, update):
    telegram_id = update.message.chat_id
    bot.send_message(chat_id=update.message.chat_id, text='oi')
    path = 'C:/Users/f3012012/Documents/TJRR/SAD_CGJ_Bot/server/webservice/'
    servidor = session.query(Servidores).filter_by(telegram_id = telegram_id).one()
    url_api = 'http://10.50.16.80:5000/{}/produtividade/atual/'.format(servidor.matricula)
    info = {'telegram_id' : telegram_id}
    r = requests.post(url=url_api, params=info)
    doc = io.BytesIO(r.content)
    doc.name = '{}.pdf'.format(datetime.date,)
    bot.send_message(chat_id=update.message.chat_id, text=r.url)
    bot.send_document(chat_id=telegram_id, document=doc)


def third(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='oi')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Para relatorio de produtividade atual diga "atual"')

atual_handler = MessageHandler(filter_atual, atual)
third_handler = MessageHandler(filter_third, third)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(atual_handler)
dispatcher.add_handler(third_handler)


updater.start_polling()
