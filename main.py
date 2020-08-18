import telebot
import logging

import maze


# TODO: Добавить инструкцию по установке программы, котороя создает лабиринт
# TODO: Добавить описание конечного продукта



# Инициализируем logging
logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("BOT")


# Инициализируем телеграм бота
bot = telebot.TeleBot("1119904996:AAHv0-cvFUWbmAClT-wzG1xkpqOAka56RL8")


# Инициализируем лабиринт
mz = maze.Maze("/home/whoman/wrk/development/c++/MazeBuilder")

# Создаем меню для управления ботом
main_menu = telebot.types.ReplyKeyboardMarkup()
main_menu.row("Ширина", "Высота")
main_menu.row("Построить лабиринт")


# Если получили команду старт, то приветсвтвуем пользователя
# и показываем ему графический интерфейс
@bot.message_handler(commands=['start'])
def start(message):
    logger.info("Start message")
    bot.send_message(message.chat.id, "Укажи параметры лабиринта.", reply_markup=main_menu)


# Если получили сообщение "Размер", то говорим пользователю, чтобы он
# указал длину, а затем ширину.
@bot.message_handler(content_types=['text'])
def reply(message):
    logger.debug("Text message [" + message.text + "] has arrived")
    if message.text == "Ширина":
        bot.send_message(message.chat.id, "Укажи ширину лабиринта...")
        bot.register_next_step_handler(message, set_width)
        logger.info("Waiting for the input of the width...")
    elif message.text == "Высота":
        bot.send_message(message.chat.id, "Укажи высоту лабиринта...")
        bot.register_next_step_handler(message, set_height)
        logger.info("Waiting for the input of the height...")
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
                          Ширина: " + str(mz.w) + "\n\
                          Высота: " + str(mz.h) + "\n\
                          Верно?",
                         reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Такой команды не существует.\n\
                                           Выбери одну из доступных!")
        logger.warning("Unknown text message")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    logger.debug("CallBack data from little keyboard is [" + call.data + "]")
    if call.data == "yes": # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, "Создаю лабиринт...")
        mz.build_maze()
        logger.info("Maze was made")
        img = open("maze.bmp", 'rb')
        bot.send_photo(call.message.chat.id, img)
        logger.info("Maze photo was sent")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Измени нужные параметры и возвращайся.")
    else:
        logger.warning("Unknown callback data")
        

def set_width(message):
    try:
        mz.set_width(int(message.text))
        logger.info("Width was changed")
        bot.send_message(message.chat.id, "Ширина изменена.")
    except ValueError:
        bot.send_message(message.chat.id, "Значение должно быть больше 3,\n \
                                           Быть числом\n \
                                           Введи новое значение!")
        bot.register_next_step_handler(message, set_width)
        return


def set_height(message):
    try:
        mz.set_height(int(message.text))
        logger.info("Height was changed")
        bot.send_message(message.chat.id, "Высота изменена.")
    except ValueError:
        bot.send_message(message.chat.id, "Значение должно быть больше 3,\n \
                                           Быть числом\n \
                                           Введи новое значение!")
        bot.register_next_step_handler(message, set_height)
        return
    


bot.polling()