import os
import time


# TODO: Сделать контроль над параметрами


class Maze():
    def __init__(self, maze_builder_path):
        self.mb_path = maze_builder_path
        self.w = 6
        self.h = 6
    
    def set_width(self, value: int):
        self.w = value

    def set_height(self, value: int):
        if value > 3:
            self.h = value

    def build_maze(self): # Построить лабиринт
        # Запускаем файл, который строит лабиринт и возращает картинку
        # Переносим данный файл в папку испольняемой программы(Бота)
        dir = os.getcwd()
        os.chdir(self.mb_path)
        os.system("./build/maze_builder -w " + str(self.w) + " -h " + str(self.h))
        time.sleep(2)
        os.chdir(dir)
        os.rename(os.path.join(self.mb_path, "maze.bmp"), os.path.join(os.getcwd(), "maze.bmp"))
