import os
import subprocess
import sys
import time


class Maze():
    def __init__(self, maze_builder_path):
        self.mb_path = maze_builder_path
        self.w = 6
        self.h = 6
    
    def set_width(self, value: int):
        self.w = value

    def set_height(self, value: int):
        self.h = value
    
    def get_width(self):
        return self.w
    
    def get_height(self):
        return self.h

    def build_maze(self): # Построить лабиринт
        # Запускаем файл, который строит лабиринт и возращает картинку
        # Переносим данный файл в папку испольняемой программы(Бота)
        if sys.platform == "win32":
            os.startfile(os.path.join(self.mb_path, "build/maze_builder"))
        else:
            dir = os.getcwd()
            os.chdir(self.mb_path)
            os.system("./build/maze_builder")
            time.sleep(2)
            os.chdir(dir)
            os.rename(os.path.join(self.mb_path, "maze.bmp"), os.path.join(os.getcwd(), "maze.bmp"))
