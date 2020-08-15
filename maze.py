class Maze():
    def __init__(self, w=6, h=6):
        self.w = w
        self.h = h
    
    def set_width(self, value: int):
        self.w = value

    def set_height(self, value: int):
        self.h = value