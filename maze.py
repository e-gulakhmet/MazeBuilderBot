import os
import time
import logging


# TODO: Сделать контроль над параметрами


class Maze():
    def __init__(self, maze_builder_path):
        self.mb_path = maze_builder_path
        self.w = 6 # Ширина
        self.h = 6 # Высота
        self.start_cell = 3 # Стартовая ячейка
        self.finish_cell = 2 # Ячейка финиша
        self.random_start_val = 0 # Значения для рандомной последовательности
        self.show_path = False # Показ пути и ответвлеий
        self.logger = logging.getLogger("MAZE")
    
    def set_width(self, value):
        if value != int:
            self.logger.warning("Width must be integer")
            return ValueError
        if value < 3:
            self.logger.warning("Width cannot be less than 3")
            return ValueError
        self.w = value
        self.logger.info("Width was set")

    def set_height(self, value: int):
        if value != int:
            self.logger.warning("Width must be integer")
        if value < 3:
            self.logger.warning("Height cannot be less than 3")
            return ValueError
        self.h = value
        self.logger.info("Height was set")

    def build_maze(self): # Построить лабиринт
        # Запускаем файл, который строит лабиринт и возращает картинку
        # Переносим данный файл в папку испольняемой программы(Бота)
        dir = os.getcwd()
        os.chdir(self.mb_path)
        p = ""
        if (self.show_path):
            p = " -p "
        os.system("./build/maze_builder -w " + str(self.w) + " -h " + str(self.h)
                  + " -s " + str(self.start_cell) + " -f " + str(self.finish_cell)
                  + " -r " + str(self.random_start_val) + p)
        self.logger.info("Maze was created")
        time.sleep(2)
        os.chdir(dir)
        os.rename(os.path.join(self.mb_path, "maze.bmp"), os.path.join(os.getcwd(), "maze.bmp"))
        self.logger.info("Maze was moved to the current directory")
