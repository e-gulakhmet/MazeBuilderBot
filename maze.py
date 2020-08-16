import os
import subprocess
import sys


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


    def build_maze(self):
        if sys.platform == "win32":
            os.startfile(os.path.join(self.mb_path, "build/maze_builder"))
        else:
            # opener = "open" if sys.platform == "darwin" else "xdg-open"
            # subprocess.call([opener, os.path.join(self.mb_path, "build/maze_builder")])

            subprocess.call([os.path.join(self.mb_path, "build/maze_builder")])

            os.rename(os.path.join(self.mb_path, "maze.bmp"), os.path.join(os.getcwd(), "maze.bmp"))
