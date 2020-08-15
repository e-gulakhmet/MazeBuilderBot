import telebot



bot = telebot.TeleBot("1119904996:AAHv0-cvFUWbmAClT-wzG1xkpqOAka56RL8")


# Если получили команду старт, то приветсвтвуем пользователя
# и показываем ему графический интерфейс
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "HelloWorld")


bot.polling()