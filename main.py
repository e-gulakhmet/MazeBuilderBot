import telebot

bot = telebot.TeleBot("1257014150:AAGPqLUQ_iXHTU3h_jOdKjcOatqVpE3xyAU")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

bot.polling()