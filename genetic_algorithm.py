from matplotlib import pyplot as plt

import numpy as np
import random
import os

"Game Rules"
BOARD_SIZE = 27
BANK_RANGE = (BOARD_SIZE - 3) // 2
POWER_RANGE = 8

HOME_FIX_OVERWRITE = True


class Game:
    def __init__(self, empty_board=False):
        # self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.score = 0
        if empty_board:
            self.board = self.empty_board()
        else:
            self.board = self.random_board()
        self.base_fields = self.initial_field_list()

        self.put_bank()
        self.base_energy_field()
        self.base_reach()

        os.makedirs('pics', exist_ok=True)
        os.makedirs('pics/debug', exist_ok=True)

    def add(self, y, x, figure):
        figure = str(figure).lower()
        if figure == 'home':
            element = Home()
        elif figure == 'tower':
            element = Tower()
        elif figure == 'road':
            element = Road()
        else:
            raise ValueError(f"Unrecognizes figure type: {figure}")

        self.board[y, x] = element

    def draw(self, save=None, debug_road=False, debug_power=False):
        """
        Function that draw board.
        If save is passed, then images is saved and not shown
        Args:
            debug: boolean, draws some debug thing
            save: string, name of file to save to

        Returns:

        """
        plt.figure(figsize=(8, 8))
        plt.grid()
        for y, row in enumerate(self.board):
            for x, element in enumerate(row):
                if type(element) is Home:
                    if element.base:
                        if element.reach:
                            color = element.color
                        else:
                            color = 'k'
                        plt.text(x - 0.1, y + 0.4, element.marker, fontsize=element.size, color=color)
                else:
                    if not debug_road and type(element) is Road and not debug_power:
                        power = self.energy[y, x]
                        plt.text(x, y, '⚡', fontsize=15, color='b' if power == 1 else 'r')
                    plt.text(x, y, element.marker, fontsize=element.size, color=element.color)

                if debug_road:
                    color = 'g' if self.reach[y, x] == 1 else 'r'
                    plt.text(x, y, '✖', fontsize=10, color=color)
                if debug_power:
                    power = self.energy[y, x]
                    plt.text(x, y, '⚡', fontsize=20, color='b' if power == 1 else 'r')

        limit = [0, 27]
        plt.xlim(limit)
        plt.ylim(limit)
        # if debug:
        #     dist = 27
        #     plt.plot([0, dist, dist, 0, 0], [0, 0, dist, dist, 0], 'k', '.-')

        if save:
            plt.savefig(f"pics/{save}.png")
            plt.close()
        else:
            plt.show()

    def put_bank(self):
        self.board[11:16, 11:16] = Road()
        self.board[12:15, 12:15] = Bank()

    def base_energy_field(self):
        self.energy = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.energy[0:27, 0:POWER_RANGE] = 1
        self.energy[0:27, 27 - POWER_RANGE:27] = 1
        self.energy[0:POWER_RANGE, 0:27] = 1
        self.energy[27 - POWER_RANGE:27, 0:27] = 1

    def base_reach(self):
        self.reach = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.reach[0, 0:27] = 1
        self.reach[26, 0:27] = 1
        self.reach[0:27, 0] = 1
        self.reach[0:27, 26] = 1

    @staticmethod
    def house_fields(a, b):
        yield a, b + 1
        yield a + 1, b
        yield a + 1, b + 1

    @staticmethod
    def initial_field_list():
        area = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        area[0:27, 0:POWER_RANGE] = 1
        area[0:27, 27 - POWER_RANGE:27] = 1
        area[0:POWER_RANGE, 0:27] = 1
        area[27 - POWER_RANGE:27, 0:27] = 1
        out = []
        for y, row in enumerate(area):
            for x, val in enumerate(row):
                if val == 1:
                    out.append((y, x))
        return out

    @staticmethod
    def reach_field(y, x):
        yield y + 1, x
        yield y - 1, x
        yield y, x + 1
        yield y, x - 1

    @staticmethod
    def power_reach_field(y, x):
        assert POWER_RANGE == 8
        #         . . . . .
        #       . . . . . .
        #     . . . . . . .
        #   . . . . . . . .
        # . . . . . . . . .
        # . . . . . . . . .
        # . . . . . . . . .
        # . . . . . . . . .
        # . . . . . . . . T
        fields = []
        for new_y in range(y - 4, y + 5):
            if new_y < 0 or new_y >= BOARD_SIZE:
                continue
            for new_x in range(x - 8, x + 9):
                fields.append((new_y, new_x))
        for new_y in range(y - 8, y + 8 + 1):
            if new_y < 0 or new_y >= BOARD_SIZE:
                continue
            for new_x in range(x - 4, x + 4 + 1):
                fields.append((new_y, new_x))
        for field in Game._power_reach_triangle(y, x):
            fields.append(field)
        return fields

    @staticmethod
    def _power_reach_triangle(y, x):
        """
        Function returns 4 corners (y,x) pair
        . . .
          . .
            .
        Args:
            y:
            x:

        Returns:

        """
        # right upper corner
        yield y + 5, x + 5
        yield y + 5, x + 6
        yield y + 5, x + 7
        yield y + 6, x + 5
        yield y + 6, x + 6
        yield y + 7, x + 5

        # right bottom corner
        yield y - 5, x + 5
        yield y - 5, x + 6
        yield y - 5, x + 7
        yield y - 6, x + 5
        yield y - 6, x + 6
        yield y - 7, x + 5

        # left bottom corner
        yield y - 5, x - 5
        yield y - 5, x - 6
        yield y - 5, x - 7
        yield y - 6, x - 5
        yield y - 6, x - 6
        yield y - 7, x - 5

        # left upper corner
        yield y + 5, x - 5
        yield y + 5, x - 6
        yield y + 5, x - 7
        yield y + 6, x - 5
        yield y + 6, x - 6
        yield y + 7, x - 5

    def validate(self):
        """
        Validation order:
            Put basic stuff:
                bank, reach, energy
            Fix Homes, missing pieces to foundation, delete single pieces
            Check road reach
            Check power map
            Assign power status
            Assign road reach
        Returns:

        """
        self.put_bank()
        self.base_energy_field()
        self.base_reach()
        self._clear_layout()
        self._check_power_and_road()
        self._apply_reach_and_power_to_home()

    def _clear_layout(self):
        """
        Clear reach and power markers
        Returns:

        """
        for y, row in enumerate(self.board):
            "Fixing homes loop"
            for x, element in enumerate(row):
                element.power = False
                element.reach = False
                if type(element) is Home:
                    if element.base:
                        if 8 < x < 15 and 8 < y < 15:
                            self.board[y, x] = Road()
                            continue
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
                                    self.board[field] = Home(base=False)
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
                        "Check pieces that are not foundation, and remove if there is no base in range"
                        try:
                            valid = type(self.board[y, x - 1]) is Home and self.board[y, x - 1].base
                        except IndexError:
                            valid = False

                        if not valid:
                            try:
                                valid = type(self.board[y - 1, x]) is Home and self.board[y - 1, x].base
                            except IndexError:
                                valid = False
                        if not valid:
                            try:
                                valid = type(self.board[y - 1, x - 1]) is Home and self.board[y - 1, x - 1].base
                            except IndexError:
                                valid = False
                        if not valid:
                            self.board[y, x] = Road()

                elif type(element) is Road:
                    pass
                elif type(element) is Tower:
                    pass
                elif type(element) is Bank:
                    pass
                elif type(element) is Figure:
                    raise ValueError("How did you get here? Base class figure is on board!")
                else:
                    raise ValueError(f"This object has unknown type: {type(element)}")

    def _check_power_and_road(self):
        """
        Creates new map of power and reach.
        Returns:

        """
        new_fields = self.base_fields.copy()
        while len(new_fields) > 0:
            fields_to_check = new_fields
            new_fields = []
            for y, x in fields_to_check:
                "Checking electricity and reach"
                element = self.board[y, x]
                if type(element) is Road:
                    if self.reach[y, x] == 1:
                        for field in self.reach_field(y, x):
                            try:
                                if self.reach[field] == 0:
                                    self.reach[field] = 1
                                    if type(self.board[field]) is Road:
                                        new_fields.append(field)
                            except IndexError:
                                pass

                elif type(element) is Tower:
                    pass
                    if not element.power and self.energy[y, x] == 1:
                        element.power = True
                        for field in self.power_reach_field(y, x):
                            try:
                                self.energy[field] = 1
                                if type(self.board[field]) is Tower:
                                    new_fields.append(field)

                            except IndexError:
                                pass

                elif type(element) is Home:
                    pass
                elif type(element) is Bank:
                    pass
                elif type(element) is Figure:
                    raise ValueError("How did you get here? Base class figure is on board!")
                else:
                    raise ValueError(f"This object has unknown type: {type(element)}")

    def _apply_reach_and_power_to_home(self):
        """
        Assigns power and reach to home foundation element
        Returns:

        """
        for y, row in enumerate(self.board):
            for x, element in enumerate(row):
                if type(element) is Home and element.base:
                    if self.energy[y, x] == 1:
                        element.power = True
                    if self.reach[y, x] == 1:
                        element.reach = True

                    if not (element.power and element.reach):
                        # print(element.power, element.reach)
                        for field in self.house_fields(y, x):
                            try:
                                if self.energy[field] == 1:
                                    element.power = True
                                if self.reach[field] == 1:
                                    element.reach = True
                            except IndexError:
                                pass

    @staticmethod
    def empty_board():
        board = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=Figure)
        for y, row in enumerate(board):
            for x, element in enumerate(row):
                board[y, x] = Road()
        return board

    @staticmethod
    def random_board():
        pool = [Road, Home, Tower]
        chance = [0.7, 0.25, 0.05]
        board = np.random.choice(pool, size=(BOARD_SIZE, BOARD_SIZE), p=chance)

        for y, row in enumerate(board):
            for x, element in enumerate(row):
                board[y, x] = board[y, x]()
        return board


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
    def __init__(self, base=True):
        super().__init__()
        self.power = False
        self.path = False
        self.marker = '▩'
        self.size = 37
        self.color = 'g'
        self.base = base

    def __repr__(self):
        return "H"


class Tower(Figure):
    def __init__(self):
        super().__init__()
        self.power_range = POWER_RANGE
        self.power = False
        self.marker = 'T'
        self.color = (0.7, 0, 0.8)

    def power_off(self):
        self.power = False
        self.color = (0.7, 0, 0.8)

    def power_on(self):
        self.power = True
        self.color = (0, 0.8, 0)

    def __repr__(self):
        return "T"


class Bank(Figure):
    def __init__(self):
        super().__init__()
        self.marker = 'B'
        self.color = (0.1, 0.6, 0.5)

    def __repr__(self):
        return "B"


if __name__ == "__main__":
    game = Game(empty_board=True)
    game.board[6, 11] = Tower()
    game.validate()
    x = 0
    game.draw(debug_power=True, save=f"{x}_fixed")
