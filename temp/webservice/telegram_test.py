from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import requests
from functools import wraps
from telegram import ChatAction, ReplyKeyboardMarkup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Servidores, Subordinados
import io
import datetime
from config import proxy_config, ip, usaProxy


engine = create_engine('sqlite:///servidores.db')#, connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

token = '650314066:AAFrittaRz9-P_rcBHGmy7jpzYsOVIueVeU'

if usaProxy:
    updater = Updater(token=token, request_kwargs=proxy_config)
else:
    updater = Updater(token=token)
dispatcher = updater.dispatcher

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)
        return command_func
    
    return decorator


class FilterAtual(BaseFilter):
    def filter(self, message):
        return 'atual' in message.text

class FilterThird(BaseFilter):
    def filter(self, message):
        return 'manda o terceiro' in message.text

class FilterServidor(BaseFilter):
    def filter(self, message):
        return 'produtividade do servidor' in message.text

filter_atual = FilterAtual()
filter_third = FilterThird()
filter_servidor = FilterServidor()

custom_keyboard = [['Produtividade atual']]
reply_markup = ReplyKeyboardMarkup(custom_keyboard)

@send_action(ChatAction.TYPING)
def atual(bot, update):
    telegram_id = update.message.chat_id
#    bot.send_message(chat_id=update.message.chat_id, text='oi')
#    path = 'C:/Users/f3012012/Documents/TJRR/SAD_CGJ_Bot/server/webservice/'
    servidor = session.query(Servidores).filter_by(telegram_id = telegram_id).one()
    url_api = 'http://{}:5000/{}/produtividade/atual/'.format(ip, servidor.matricula)
    info = {'telegram_id' : telegram_id}
    r = requests.post(url=url_api, params=info)
    doc = io.BytesIO(r.content)
    r = requests.get(url=url_api, params=info)
    doc.name = r.text
    bot.send_message(chat_id=update.message.chat_id, text='OK. Enviando produtividade atual do {} {}.'.format(servidor.cargo, servidor.nome))
    bot.send_document(chat_id=telegram_id, document=doc)


def third(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='oi')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Para relatorio de produtividade atual para o ID {} utilize o botão abaixo'.format(update.message.chat_id), reply_markup=reply_markup)

def prodServ(bot, update):
    telegram_id = update.message.chat_id
    magistrado = session.query(Servidores).filter_by(telegram_id = telegram_id).one()
    marcador = update.message.text.find('f30')
    matricula_servidor = update.message.text[marcador:(marcador+8)]
    bot.send_message(chat_id=update.message.chat_id, text='a matricula do servidor e {}?'.format(matricula_servidor))
    subordinados = session.query(Subordinados).filter_by(magistrado = magistrado.matricula).all()
    print(subordinados)
    for subordinado in subordinados:
        if subordinado.matricula == matricula_servidor:
            url_api = 'http://{}:5000/{}/produtividade/atual/'.format(ip, subordinado.matricula)
            info = {'telegram_id' : telegram_id, 'sub' : 't'}
            r = requests.post(url=url_api, params=info)
            doc = io.BytesIO(r.content)
            r = requests.get(url=url_api, params=info)
            doc.name = r.text
            bot.send_message(chat_id=update.message.chat_id, text='OK. Enviando produtividade atual do {} {}.'.format(subordinado.cargo, subordinado.nome))
            bot.send_document(chat_id=telegram_id, document=doc)
            return
    bot.send_message(chat_id=update.message.chat_id, text='Desculpe. permissao negada ou servidor nao encontrado')
        







atual_handler = MessageHandler(filter_atual, atual)
third_handler = MessageHandler(filter_third, third)
servidor_handler = MessageHandler(filter_servidor, prodServ)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(atual_handler)
dispatcher.add_handler(servidor_handler)
dispatcher.add_handler(third_handler)


updater.start_polling()
