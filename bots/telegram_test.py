from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter


updater = Updater(token='650314066:AAFrittaRz9-P_rcBHGmy7jpzYsOVIueVeU')
dispatcher = updater.dispatcher

class FilterOutro(BaseFilter):
    def filter(self, message):
        return 'manda o outro' in message.text

class FilterThird(BaseFilter):
    def filter(self, message):
        return 'manda o terceiro' in message.text

filter_outro = FilterOutro()
filter_third = FilterThird()

def outro(bot, update):
    bot.send_document(chat_id=update.message.chat_id, document=open('outro_documentao.txt', 'rb'))


def third(bot, update):
    bot.send_document(chat_id=update.message.chat_id, document=open('terceiro_documentao.txt', 'rb'))


def start(bot, update):
    bot.send_document(chat_id=update.message.chat_id, document=open('documentao_massa.txt', 'rb'))

outro_handler = MessageHandler(filter_outro, outro)
third_handler = MessageHandler(filter_third, third)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(outro_handler)
dispatcher.add_handler(third_handler)


updater.start_polling()