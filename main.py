import telebot

import maze



bot = telebot.TeleBot("1119904996:AAHv0-cvFUWbmAClT-wzG1xkpqOAka56RL8")

mz = maze.Maze()

main_menu = telebot.types.ReplyKeyboardMarkup()
main_menu.row("Размер")


# Если получили команду старт, то приветсвтвуем пользователя
# и показываем ему графический интерфейс
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row("Размер")

    bot.send_message(message.chat.id, "Укажи параметры лабиринта.", reply_markup=main_menu)


# Если получили сообщение "Размер", то говорим пользователю, чтобы он
# указал длину, а затем ширину.
@bot.message_handler(content_types=['text'])
def reply(message):
    if message.text == 'Размер':
        bot.send_message(message.chat.id, "Укажи ширину")
        bot.register_next_step_handler(message, set_width)


def set_width(message):
    value = int(message.text)
    mz.set_width(value)
    bot.send_message(message.chat.id, "Укажи высоту")
    bot.register_next_step_handler(message, set_height)


def set_height(message):
    value = int(message.text)
    mz.set_height(value)
    bot.send_message(message.chat.id, "Теперь можешь указать остальные(необязательные) параметры")
    


bot.polling()

