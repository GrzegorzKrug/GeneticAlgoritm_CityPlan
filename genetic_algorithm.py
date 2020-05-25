from matplotlib import pyplot as plt

import random
import time
import pandas as pd
import math
import datetime
import numpy as np

BOARD_SIZE = 27


class Game:
    def __init__(self):
        # self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.score = 0
        self.random_board()

    def draw(self):
        plt.figure(figsize=(8, 8))
        for y, row in enumerate(self.board):
            for x, element in enumerate(row):
                if type(element) is Home:
                    fontsize = 50
                else:
                    fontsize = 20
                plt.text(x, y, element.marker, fontsize=fontsize, color=element.color)

        plt.xlim([-1, 28])
        plt.ylim([-1, 28])
        plt.grid()
        plt.show()

    def validate(self):
        pass

    def random_board(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=Figure)
        pool = [Road, Home, Tower]
        chance = 1 / len(pool)

        for y, row in enumerate(self.board):
            for x, element in enumerate(row):
                roll = np.random.rand()
                selection = 0
                while roll > chance:
                    roll -= chance
                    selection += 1
                self.board[x, y] = pool[selection]()


class Figure:
    def __init__(self):
        super()
        self.marker = '.'
        self.color = 'w'

    def __repr__(self):
        return "F"


class Road(Figure):
    def __init__(self):
        super().__init__()
        self.marker = '.'
        self.color = 'w'

    def __repr__(self):
        return "."


class Home(Figure):
    def __init__(self):
        super().__init__()
        self.power = False
        self.path = False
        self.position = None
        self.marker = '⌂'
        self.color = 'g'

    def __repr__(self):
        return "H"


class Tower(Figure):
    def __init__(self):
        super().__init__()
        self.position = None
        self.power = False
        self.marker = '⚡'
        self.color = 'b'

    def __repr__(self):
        return "T"


class Bank(Figure):
    def __init__(self):
        pass

    def __repr__(self):
        return "B"


if __name__ == "__main__":
    game = Game()
    game.draw()
