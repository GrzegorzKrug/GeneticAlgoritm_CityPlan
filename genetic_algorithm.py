from matplotlib import pyplot as plt

import os
import numpy as np

"Game Rules"
BOARD_SIZE = 27
BANK_RANGE = (BOARD_SIZE - 3) // 2
POWER_RANGE = 7

HOME_FIX_OVERWRITE = True


class Game:
    def __init__(self):
        # self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.score = 0
        self.random_board()
        os.makedirs('pics', exist_ok=True)
        os.makedirs('pics/debug', exist_ok=True)

    def draw(self, debug=False, save=None):
        plt.figure(figsize=(8, 8))
        for y, row in enumerate(self.board):
            for x, element in enumerate(row):
                if debug:
                    plt.text(x, y, "o", fontsize=10)
                if type(element) is Home:
                    if element.base:
                        plt.text(x - 0.2, y + 0.3, element.marker, fontsize=element.size, color=element.color)
                    # else:
                    #     plt.text(x - 0.2, y + 0.3, element.marker, fontsize=20, color='k')
                else:
                    plt.text(x, y, element.marker, fontsize=element.size, color=element.color)
        if debug:
            dist = 27
            plt.plot([0, dist, dist, 0, 0], [0, 0, dist, dist, 0], 'k', '.-')
        plt.xlim([-1, 28])
        plt.ylim([-1, 28])
        plt.grid()
        if save:
            plt.savefig(f"pics/{save}.png")
            plt.close()
        else:
            plt.show()

    @staticmethod
    def house_fields(x, y):
        yield x, y + 1
        yield x + 1, y
        yield x + 1, y + 1

    def validate(self):
        for y, row in enumerate(self.board):
            for x, element in enumerate(row):
                if type(element) is Home:
                    if element.base:
                        try:
                            for field in self.house_fields(y, x):
                                assert type(self.board[field]) is Home and self.board[field].base is False
                            valid = True
                        except (KeyError, AssertionError):
                            valid = False
                        except IndexError:
                            self.board[y, x] = Road()
                            continue

                        if not valid and HOME_FIX_OVERWRITE:
                            try:
                                for field in self.house_fields(y, x):
                                    self.board[field] = Home()
                                try:
                                    check_field = (y + 1, x - 1)
                                    if type(self.board[check_field]) is Home and self.board[check_field].base:
                                        self.board[check_field] = Road()
                                except IndexError:
                                    pass
                            except IndexError:
                                self.board[y, x] = Road()

                        elif not valid:
                            self.board[y, x] = Road()
                    else:
                        pass
                        # raise NotImplementedError

                elif type(element) is Road:
                    pass
                elif type(element) is Tower:
                    pass
                elif type(element) is Figure:
                    raise ValueError("How did you get here? Base class figure is on board!")
                else:
                    raise ValueError(f"This object has unknown type: {type(element)}")

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

                figure = pool[selection]()
                if type(figure) is Home:
                    figure.base = True
                self.board[x, y] = figure


class Figure:
    def __init__(self):
        super()
        self.marker = ''
        self.color = 'k'
        self.size = 20

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
    def __init__(self, base=False):
        super().__init__()
        self.power = False
        self.path = False
        self.position = None
        self.marker = '⌂'
        self.marker = '▩'
        self.size = 37
        self.color = 'g'
        self.base = base

    def __repr__(self):
        return "H"


class Tower(Figure):
    def __init__(self):
        super().__init__()
        self.position = None
        self.power = False
        self.marker = '⚡'
        self.color = 'b'

        self.power_range = POWER_RANGE

    def __repr__(self):
        return "T"


class Bank(Figure):
    def __init__(self):
        pass

    def __repr__(self):
        return "B"


if __name__ == "__main__":
    game = Game()
    game.draw(save='0')
    game.validate()
    game.draw(save='1')
    # game.validate()
    # game.draw(save='2')
    # game.validate()
    # game.draw(save='3')
