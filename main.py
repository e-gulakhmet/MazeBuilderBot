import telebot
import logging
import re

import maze


# TODO: Добавить инлаин функции
# TODO: Добавить argparser
# TODO: Обработать ошибки, связанные с запуском MazeBuider



# Инициализируем logging
logging.basicConfig(filename="logging.log", level=logging.INFO, format="%(asctime)s %(name)s [%(levelname)s] : %(message)s")
logger = logging.getLogger("BOT")


# Инициализируем телеграм бота
bot = telebot.TeleBot("1119904996:AAHv0-cvFUWbmAClT-wzG1xkpqOAka56RL8")


# Инициализируем лабиринт
mz = maze.Maze("/home/whoman/wrk/development/c++/MazeBuilder")

# Создаем меню для управления ботом
main_menu = telebot.types.ReplyKeyboardMarkup()
main_menu.row("Размеры", "Старт", "Финиш", "Подсвечивание пути")
main_menu.row("Построить лабиринт")

# Создаю регулярное выражение, которое будет 
# реагировать на корректный ввод инлаин функций
digits_pattern = re.compile(r'^[0-9]+ [0-9]+$', re.MULTILINE)


# Если получили команду старт, то приветсвтвуем пользователя
# и показываем ему графический интерфейс
@bot.message_handler(commands=['start'])
def start(message):
    logger.info("Start message")
    bot.send_message(message.chat.id, "Укажи параметры лабиринта.", reply_markup=main_menu)


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    matches = re.match(digits_pattern, query.query)
    try:
        w, h = matches.group().split()
        logger.info("Parameters was set from inline call")
    # Вылавливаем ошибку, если вдруг юзер ввёл чушь
    # или задумался после ввода первого числа
    except AttributeError as ex:
        return


    mz.set_width(int(w))
    mz.set_height(int(h))
    mz.build_maze()
    logger.info("Maze was built")
    img = open("maze.bmp", 'rb')
    bot.answer_inline_query(query.id, "test", cache_time=2147483646)
    logger.info("Maze image was sent")



# Если получили сообщение "Размер", то говорим пользователю, чтобы он
# указал длину, а затем ширину.
@bot.message_handler(content_types=['text'])
def reply(message):
    logger.debug("Text message [" + message.text + "] has arrived")
    if message.text == "Размеры":
        # Выводим новую клавиатуру
        size_menu = telebot.types.ReplyKeyboardMarkup()
        size_menu.row("Ширина", "Высота")
        size_menu.row("Вернуться")
        bot.send_message(message.chat.id,
                         "Выбери, какой параметр ты хочешь изменить.",
                         reply_markup=size_menu)
        logger.info("Size menu was opened")
    elif message.text == "Ширина":
        # Ожидаем ответа от пользователя,
        # он должен ввести ширину лабиринта
        bot.send_message(message.chat.id, "Укажи ширину лабиринта...")
        # Следующее присланное сообщение
        # будет обработано в функции "set_width"
        bot.register_next_step_handler(message, set_width)
        logger.info("Waiting for the input of the width...")
    elif message.text == "Высота":
        bot.send_message(message.chat.id, "Укажи высоту лабиринта...")
        bot.register_next_step_handler(message, set_height)
        logger.info("Waiting for the input of the height...")
    elif message.text == "Вернуться":
        bot.send_message(message.chat.id, "Возвращаемся...", reply_markup=main_menu)
        logger.info("Returned to the main menu")

    elif message.text == "Старт":
        bot.send_message(message.chat.id,
                         "Стартовая ячейка всегда \
                         находится на левой стороне. \
                         Укажи её(отсчёт начинается сверху)")
        bot.register_next_step_handler(message, set_start)
        logger.info("Waiting for the input of the start cell...")
    elif message.text == "Финиш":
        bot.send_message(message.chat.id,
                         "Ячейка финиша всегда \
                         находится на правой стороне. \
                         Укажи её(отсчёт начинается сверху)")
        bot.register_next_step_handler(message, set_finish)
        logger.info("Waiting for the input of the finish cell...")
    elif message.text == "Подсвечивание пути":
        # Создаем клавиатуру, которую затем прикрепим к сообщению
        kboard = telebot.types.InlineKeyboardMarkup()
        # Кнопки клавиатуры
        k_yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="path_yes")
        k_no = telebot.types.InlineKeyboardButton(text="Нет", callback_data="path_no")
        kboard.add(k_yes)
        kboard.add(k_no)   
        bot.send_message(message.chat.id,
                         "Путь и ветвления будут подсвечиваться \n \
                         Ты хочешь включить эту функцию?",
                         reply_markup=kboard)
        logger.info("Waiting for the answer...")
    elif message.text == "Построить лабиринт":
        # Создаем клавиатуру, которую затем прикрепим к сообщению
        kboard = telebot.types.InlineKeyboardMarkup()
        # Кнопки клавиатуры
        k_yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="maze_yes")
        k_no = telebot.types.InlineKeyboardButton(text="Нет", callback_data="maze_no")
        kboard.add(k_yes)
        kboard.add(k_no)   
        bot.send_message(message.chat.id,
                         "Лабиринт будет создан со следующими параметрами:\n \
                          Ширина: " + str(mz.w) + "\n\
                          Высота: " + str(mz.h) + "\n\
                          Ячейка старта: " + str(mz.start) + "\n\
                          Ячейка выхода: " + str(mz.finish) + "\n\
                          Подсвечивание пути и ветвлений: " + str(mz.path) + "\n\
                          Верно?",
                         reply_markup=kboard)
    else:
        bot.send_message(message.chat.id, "Такой команды не существует.\n \
                                           Выбери одну из доступных!")
        logger.warning("Unknown text message")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    logger.debug("CallBack data from little keyboard is [" + call.data + "]")
    if call.data == "maze_yes": # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, "Создаю лабиринт...")
        mz.build_maze()
        logger.info("Maze was made")
        img = open("maze.bmp", 'rb')
        bot.send_photo(call.message.chat.id, img)
        logger.info("Maze photo was sent")
    elif call.data == "maze_no":
        bot.send_message(call.message.chat.id, "Измени нужные параметры и возвращайся.")

    elif call.data == "path_yes":
        bot.send_message(call.message.chat.id, "Подсветка пути включена.")
        mz.path(True)
    elif call.data == "path_no":
        bot.send_message(call.message.chat.id, "Путь подсвечиваться не будет.")

    else:
        logger.warning("Unknown callback data")
        

def set_width(message):
    value = 0
    try:
        value = int(message.text)
    except ValueError:
        logger.warning("Width must be integer")
        bot.send_message(message.chat.id, "Значение должно быть числом.")
        bot.register_next_step_handler(message, set_width)
        return

    if mz.set_width(value) is False:
        bot.send_message(message.chat.id, "Значение должно быть больше 3.")
        bot.register_next_step_handler(message, set_width)
        return

    logger.info("Width was changed")
    bot.send_message(message.chat.id, "Ширина изменена.")



def set_height(message):
    value = 0
    try:
        value = int(message.text)
    except ValueError:
        logger.warning("Height must be integer")
        bot.send_message(message.chat.id, "Значение должно быть числом.")
        bot.register_next_step_handler(message, set_height)
        return

    if mz.set_height(value) is False:
        bot.send_message(message.chat.id, "Значение должно быть больше 3.")
        bot.register_next_step_handler(message, set_height)
        return

    logger.info("Height was changed")
    bot.send_message(message.chat.id, "Высота изменена.")



def set_start(message):
    value = 0
    try:
        value = int(message.text)
    except ValueError:
        logger.warning("Start cell must be integer")
        bot.send_message(message.chat.id, "Значение должно быть числом.")
        bot.register_next_step_handler(message, set_start)
        return
    if mz.set_start_cell(value) is False:
        bot.send_message(message.chat.id, "Значение должно быть больше 0 и меньше высоты.")
        bot.register_next_step_handler(message, set_start)
        return

    logger.info("Start cell was changed")
    bot.send_message(message.chat.id, "Стартовая ячейка изменена.")


def set_finish(message):
    value = 0
    try:
        value = int(message.text)
    except ValueError:
        logger.warning("Finish cell must be integer")
        bot.send_message(message.chat.id, "Значение должно быть числом.")
        bot.register_next_step_handler(message, set_finish)
        return
    if mz.set_finish_cell(value) is False:
        bot.send_message(message.chat.id, "Значение должно быть больше 0 и меньше высоты.")
        bot.register_next_step_handler(message, set_finish)
        return

    logger.info("Finish cell was changed")
    bot.send_message(message.chat.id, "Ячейка финиша изменена.")


bot.polling()