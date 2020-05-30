from matplotlib import pyplot as plt

import datetime
import numpy as np
import random
import time
import os

"Game Rules"
BOARD_SIZE = 29
OUTER_ROAD_WIDTH = 1
POWER_RANGE = 8

HOME_SCORE = 10
ROAD_SCORE = 0
TOWER_SCORE = -10

HOME_FIX_OVERWRITE = True


class Game:
    def __init__(self, empty_board=False):
        if empty_board:
            self.board = self.empty_board()
        else:
            self.board = self.random_board()
        self.base_fields = self.initial_field_list()

        self.home_count = 0

        self.put_bank()
        self.base_energy_field()
        self.base_reach()

    def add(self, y, x, figure):
        figure = str(figure).lower()
        if figure == 'home':
            element = Home()
        elif figure == 'tower':
            element = Tower()
        elif figure == 'road':
            element = Road()
        elif figure == 'random':
            pool = [Road, Home, Tower]
            element = np.random.choice(pool, size=1, p=(0.4, 0.55, 0.05))[0]()
        else:
            raise ValueError(f"Unrecognized figure type: {figure}")

        self.board[y, x] = element

    def draw(self, save=None, debug_road=False, debug_power=False, more_text=None):
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
        os.makedirs(f"{os.path.dirname(os.path.abspath(save))}", exist_ok=True)
        score = self.score()
        for y, row in enumerate(self.board):
            for x, element in enumerate(row):
                if type(element) is Home:
                    if element.base:
                        if not element.reach:
                            color = 'k'
                        elif not element.power:
                            color = 'r'
                        else:
                            color = element.color
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

        limit = [0, BOARD_SIZE]
        plt.xlim(limit)
        plt.ylim(limit)
        if more_text:
            plt.title(f"{more_text}\nHome count: {self.home_count}\nScore: {score}")
        else:
            plt.title(f"Home count: {self.home_count}\nScore: {score}")

        if save:
            plt.savefig(f"{save}.png")
            plt.close()
        else:
            plt.show()

    def put_bank(self):
        self.board[12:17, 12:17] = Road()
        self.board[13:16, 13:16] = Bank()

    def base_energy_field(self):
        self.energy = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.energy[0:BOARD_SIZE, 0] = 1
        self.energy[0:BOARD_SIZE, BOARD_SIZE - 1] = 1
        self.energy[0, 0:BOARD_SIZE] = 1
        self.energy[BOARD_SIZE - 1, 0:BOARD_SIZE] = 1

    def base_reach(self):
        self.reach = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.reach[0:BOARD_SIZE, 0] = 1
        self.reach[0:BOARD_SIZE, BOARD_SIZE - 1] = 1
        self.reach[0, 0:BOARD_SIZE] = 1
        self.reach[BOARD_SIZE - 1, 0:BOARD_SIZE] = 1

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
                        if y == 0 or y == 27 \
                                or x == 0 or x == 27 \
                                or 10 < x < 17 and 10 < y < 17:
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
                            except IndexError:
                                self.board[y, x] = Road()
                                continue

                        elif not valid:
                            self.board[y, x] = Road()
                            continue
                        try:
                            check_field = (y + 1, x - 1)
                            if type(self.board[check_field]) is Home and self.board[check_field].base:
                                self.board[check_field] = Road()
                        except IndexError:
                            pass

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
                    if not 13 <= y < 16 or not 13 <= x < 16:
                        self.board[y, x] = Road()
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

    def score(self):
        score = 0
        self.home_count = 0
        self.validate()
        for y, row in enumerate(self.board):
            for x, element in enumerate(row):
                if type(element) is Home and element.base and element.power and element.reach:
                    score += HOME_SCORE
                    self.home_count += 1
                elif type(element) is Tower:
                    score += TOWER_SCORE
                elif type(element) is Road:
                    score += ROAD_SCORE
        return score


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


class Evolution:
    def __init__(self, name, pool_size=100,
                 shuffle_chance=0.6, shuffle_ammount_random=10,
                 move_area_chance=0.3,
                 clone_chance=0.1,
                 swap_chance=0.05,
                 drop_chance=0.15, drop_ammount_flat=0.1, drop_every=250):
        self.pool_size = pool_size
        self.shuffle_chance = shuffle_chance
        self.shuffle_ammount_random = shuffle_ammount_random
        self.move_area_chance = move_area_chance
        self.clone_chance = clone_chance
        self.swap_chance = swap_chance
        self.drop_chance = drop_chance
        self.drop_ammount_flat = drop_ammount_flat
        self.drop_every = drop_every

        self.name = name
        dt = datetime.datetime.timetuple(datetime.datetime.now())
        self.run_time = f"{dt.tm_mon:>02}-{dt.tm_mday:>02}--" \
                        f"{dt.tm_hour:>02}-{dt.tm_min:>02}-{dt.tm_sec:>02}"
        os.makedirs(name, exist_ok=True)
        self.pool = []
        pool = self.load_pool()

        if pool:
            self.pool = pool
        self.fill_pool()
        self.sort_pool()
        self.refresh_score()

    def sort_pool(self):
        self.pool.sort(key=lambda x: x[1], reverse=True)

    def fill_pool(self):
        while len(self.pool) < self.pool_size:
            self.pool.append(self.random_pool())

    def print_scores(self, n):
        for inde, game in enumerate(self.pool):
            if n < inde:
                break
            print(game[1])

    def refresh_score(self):
        self.pool = [(game, game.score()) for game, score in self.pool]

    def get_scores(self):
        scores = []
        for game, score in self.pool:
            scores.append(score)
        return scores

    @staticmethod
    def random_pool():
        game = Game()
        score = game.score()
        return game, score

    def draw_best(self, n=1):
        for x in range(n):
            self.pool[x][0].draw(save=f"{self.name}/best_{x}")

    def save_pool(self, filepath=None):
        if filepath:
            save_to = filepath
        else:
            save_to = f'{self.name}/evolution_pool'
        np.save(save_to, self.pool)
        print(f"Saved pool: {save_to}")

    def clone(self):
        """
        Clones random fragments of target board, size is also random
        Returns:

        """
        for ind, (game, score) in enumerate(self.pool):
            if random.random() < self.clone_chance:
                new_game = Game(empty_board=True)
                new_game.board = game.board.copy()

                target_id = np.random.randint(0, self.pool_size)
                while target_id == ind:
                    target_id = np.random.randint(0, self.pool_size)

                y_min, y_max, x_min, x_max = 0, 0, 0, 0
                while y_min == y_max or x_min == x_max:
                    # "Iterate until y's and x's are different
                    target = np.random.randint(0, BOARD_SIZE, 4)
                    y_min, y_max, x_min, x_max = target
                    if y_min > y_max:
                        y_min, y_max = y_max, y_min
                    if x_min > x_max:
                        x_min, x_max = x_max, x_min

                target_board = self.pool[target_id][0].board.copy()
                new_game.board[y_min:y_max, x_min:x_max] = target_board[y_min:y_max, x_min:x_max]
                new_score = new_game.score()
                if new_score >= score:
                    game.board = new_game.board.copy()
                    self.pool[ind] = (game, new_score)

    def shuffle(self):
        """
        Puts random pieces in random places
        Returns:

        """
        for ind, (game, score) in enumerate(self.pool):
            if random.random() < self.shuffle_chance:
                new_game = Game(empty_board=True)
                new_game.board = game.board.copy()

                for _ in range(np.random.randint(1, self.shuffle_ammount_random)):
                    y, x = np.random.randint(0, BOARD_SIZE, 2)
                    new_game.add(y, x, 'random')

                new_score = new_game.score()
                if new_score >= score:
                    game.board = new_game.board.copy()
                    self.pool[ind] = (game, new_score)

    def move_areas(self):
        """
        Swaps random pieces on board
        Returns:

        """
        for ind, (game, score) in enumerate(self.pool):
            if random.random() < self.move_area_chance:
                new_game = Game(empty_board=True)
                new_game.board = game.board.copy()

                index_y, index_x = 0, 0
                direction_y, direction_x = 0, 0
                size_y, size_x = 0, 0
                while not 0 <= index_y + size_y < BOARD_SIZE \
                        or not 0 <= index_y + direction_y + size_y < BOARD_SIZE \
                        or not 0 <= index_y + direction_y < BOARD_SIZE \
                        or not 0 <= index_x + size_x < BOARD_SIZE \
                        or not 0 <= index_x + direction_x + size_x < BOARD_SIZE \
                        or not 0 <= index_x + direction_x < BOARD_SIZE \
                        or not direction_y and not direction_x:
                    index_y, index_x = np.random.randint(0, BOARD_SIZE, 2)
                    direction_y, direction_x = np.random.randint(-2, 3, 2)
                    size_y, size_x = np.random.randint(1, BOARD_SIZE // 4, 2)

                for curr_y in range(0, size_y):
                    for curr_x in range(0, size_x):
                        new_game.board[index_y + curr_y, index_x + curr_x] = Road()

                new_game.board[index_y + direction_y:index_y + direction_y + size_y,
                index_x + direction_x:index_x + direction_x + size_x] = \
                    game.board[index_y:index_y + size_y, index_x:index_x + size_x].copy()

                new_score = new_game.score()
                if new_score >= score:
                    game.board = new_game.board.copy()
                    self.pool[ind] = (game, new_score)

    def swap(self):
        """
        Swaps random pieces on board
        Returns:

        """
        for ind, (game, score) in enumerate(self.pool):
            if random.random() < self.swap_chance:
                new_game = Game(empty_board=True)
                new_game.board = game.board.copy()

                dist_y, dist_x = np.random.randint(0, BOARD_SIZE // 2, 2) + 1

                from_y, from_x, to_y, to_x = 0, 0, 0, 0
                while abs(from_y - to_y) < dist_y or abs(from_x - to_x) < dist_x \
                        or from_y + dist_y >= BOARD_SIZE \
                        or from_x + dist_x >= BOARD_SIZE \
                        or to_y + dist_y >= BOARD_SIZE \
                        or to_x + dist_x >= BOARD_SIZE:
                    from_y, from_x, to_y, to_x = np.random.randint(0, BOARD_SIZE, 4)
                # From - > Temp
                # To -> From
                # Temp -> To
                temp = new_game.board[from_y:from_y + dist_y, from_x:from_x + dist_x].copy()
                new_game.board[from_y:from_y + dist_y, from_x:from_x + dist_x] = new_game.board[to_y:to_y + dist_y,
                                                                                 to_x:to_x + dist_x].copy()
                new_game.board[to_y:to_y + dist_y, to_x:to_x + dist_x] = temp
                new_score = new_game.score()
                if new_score >= score:
                    game.board = new_game.board.copy()
                    self.pool[ind] = (game, new_score)

    def dropout(self):
        self.pool = self.pool[:int(len(self.pool) * (1 - self.drop_ammount_flat))]
        self.pool = [obj for ind, obj in enumerate(self.pool) if random.random() > self.drop_chance or ind == 0]

    def load_pool(self, filepath=None):
        if filepath:
            load_from = filepath
        else:
            load_from = f'{self.name}/evolution_pool.npy'
        try:
            pool = list(np.load(load_from, allow_pickle=True))
        except FileNotFoundError:
            print(f"Not found pool: {load_from}")
            pool = None
        return pool

    @staticmethod
    def moving_average(array, window_size=None, agents_num=1):
        size = len(array)

        if not window_size or window_size and size < window_size:
            window_size = size // 20

        while len(array) % window_size or window_size % agents_num:
            window_size -= 1
            if window_size < 1:
                window_size = 1
                break

        output = []

        for sample_num in range(agents_num - 1, len(array), agents_num):
            if sample_num < window_size:
                output.append(np.mean(array[:sample_num + 1]))
            else:
                output.append(np.mean(array[sample_num - window_size: sample_num + 1]))

        if len(array) % window_size:
            output.append(np.mean(array[-window_size:]))

        return output

    def evolution(self, epoch=100):
        stats = {'epoch': [], 'max': [], 'pool_avg': [], 'scores': []}
        time0 = time.time()
        for x in range(epoch):
            if not x % 100 and x != 0:
                self.save_pool()
            self.fill_pool()

            self.clone()
            self.shuffle()
            # self.swap()
            self.move_areas()
            self.sort_pool()

            if not x % self.drop_every and x != 0:
                self.dropout()

            stats['epoch'] += [x] * len(self.pool)
            current_scores = self.get_scores()
            stats['scores'] += current_scores
            avg = np.mean(current_scores)
            stats['pool_avg'].append(avg)
            print(f"Epoch {x:<5} ended with avg: {avg:>8.2f}, "
                  f"good_homes: {self.pool[0][0].home_count:>3}, best: {np.max(current_scores):<7.2f}")

        print(f"Evolution took: {(time.time() - time0) / 60:<4.2f} min")
        plt.figure(figsize=(16, 9))
        plt.scatter(stats['epoch'], stats['scores'], c='m', alpha=0.1, s=10, label='Scores')
        plt.plot(stats['pool_avg'], c='b', label='local_avg', linewidth=2)
        plt.plot(self.moving_average(stats['pool_avg'], agents_num=1),
                 c=(0.1, 1, 0.3), label='global_avg', linewidth=4)
        plt.legend(loc='best')
        plt.savefig(f"{self.name}/stats_{self.run_time}")


if __name__ == "__main__":
    name = "run_10"
    alg1 = Evolution(name, pool_size=50, drop_every=250)
    alg1.evolution(10000)
    alg1.save_pool()
    alg1.print_scores(15)
    alg1.draw_best(15)
