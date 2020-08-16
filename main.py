import telebot

import maze


# Инициализируем телеграм бота
bot = telebot.TeleBot("1119904996:AAHv0-cvFUWbmAClT-wzG1xkpqOAka56RL8")

# Инициализируем лабиринт
mz = maze.Maze()

# Создаем меню для управления ботом
main_menu = telebot.types.ReplyKeyboardMarkup()
main_menu.row("Ширина", "Высота")
main_menu.row("Построить лабиринт")


# Если получили команду старт, то приветсвтвуем пользователя
# и показываем ему графический интерфейс
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Укажи параметры лабиринта.", reply_markup=main_menu)


# Если получили сообщение "Размер", то говорим пользователю, чтобы он
# указал длину, а затем ширину.
@bot.message_handler(content_types=['text'])
def reply(message):
    if message.text == "Ширина":
        bot.send_message(message.chat.id, "Укажи ширину лабиринта")
        bot.register_next_step_handler(message, set_width)
    elif message.text == "Высота":
        bot.send_message(message.chat.id, "Укажи высоту лабиринта")
        bot.register_next_step_handler(message, set_height)
    elif message.text == "Построить лабиринт":
        # Создаем клавиатуру, которую затем прикрепим к сообщению
        keyboard = telebot.types.InlineKeyboardMarkup()
        # Кнопки клавиатуры
        k_yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="yes")
        k_no = telebot.types.InlineKeyboardButton(text="Нет", callback_data="no")
        keyboard.add(k_yes)
        keyboard.add(k_no)

        bot.send_message(message.chat.id,
                         "Лабиринт будет создан со следующими параметрами:\n \
                          Ширина: " + str(mz.get_width()) + ";\n\
                          Высота: " + str(mz.get_height()) + ";\n\
                          Верно?",
                         reply_markup=keyboard)
    else:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "yes": # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, "Создаю лабиринт...")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Измени нужные параметры и возвращайся")


def set_width(message):
    value = int(message.text)
    mz.set_width(value)
    bot.send_message(message.chat.id, "Ширина изменена", reply_markup=main_menu)


def set_height(message):
    value = int(message.text)
    mz.set_height(value)
    bot.send_message(message.chat.id, "Высота изменена", reply_markup=main_menu)


bot.polling()