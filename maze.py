import os
import time
import logging


# TODO: Сделать контроль над параметрами


class Maze():
    def __init__(self, maze_builder_path="/home/whoman/wrk/development/c++/MazeBuilder"):
        self.mb_path = maze_builder_path
        self.w = 6 # Ширина
        self.h = 6 # Высота
        self.start_cell = 3 # Стартовая ячейка
        self.finish_cell = 2 # Ячейка финиша
        self.random_start_val = 0 # Значения для рандомной последовательности
        self.path = False # Показ пути и ответвлеий
        self.logger = logging.getLogger("MAZE")
    
    def set_width(self, value):
        if value < 3:
            self.logger.warning("Width must be less than 3")
            return False

        self.w = value
        self.logger.info("Width was set")
        return True

    def set_height(self, value):
        if value < 3:
            self.logger.warning("Height cannot be less than 3")
            return False
        self.h = value
        self.logger.info("Height was set")
        return True

    def set_start_cell(self, value):
        if value < 0 or value > self.h:
            self.logger.warning("Start cell must be less than height of maze")
            return False
        self.start_cell = value
        self.logger.info("Start cell was set")
        return True
    
    def set_finish_cell(self, value: int):
        if value < 0 or value > self.h:
            self.logger.warning("Finish cell must be less than height of maze")
            return False
        self.finish_cell = value
        self.logger.info("Finish cell was set")
        return True

    def path(self, state):
        self.path = state
        self.logger.info("Path state was set")
        return True
    


    def build_maze(self): # Построить лабиринт
        # Запускаем файл, который строит лабиринт и возращает картинку
        # Переносим данный файл в папку испольняемой программы(Бота)
        dir = os.getcwd()
        os.chdir(self.mb_path)
        p = ""
        if (self.path):
            p = " -p "
        os.system("./build/maze_builder -w " + str(self.w) + " -h " + str(self.h) +
                  " -s " + str(self.start_cell) + " -f " + str(self.finish_cell) +
                  p)
        self.logger.info("Maze was created")
        time.sleep(2)
        os.chdir(dir)
        try:
            os.rename(os.path.join(self.mb_path, "maze.bmp"), os.path.join(os.getcwd(), "maze.bmp"))
        except FileNotFoundError:
            self.logger.error("Maze was not found")
        self.logger.info("Maze was moved to the current directory")
