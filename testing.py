from genetic_algorithm import Game
import os

os.makedirs("pics/test", exist_ok=True)


def test1():
    game = Game(empty_board=True)
    y = 7
    x = 8
    game.add(y, x, 'tower')
    game.validate()
    game.draw(debug_power=True, save="test/1")

    assert game.energy[y + 2, x + 9] == 0
    assert game.energy[y + 8, x] == 1
    assert game.energy[y + 9, x] == 0
    assert game.energy[y + 8, x + 4] == 1
    assert game.energy[y + 8, x + 5] == 0
    assert game.energy[y + 7, x + 5] == 1
    assert game.energy[y + 6, x + 6] == 1
    assert game.energy[y + 7, x + 6] == 0
    assert game.energy[y + 6, x + 7] == 0


def test2():
    game = Game(empty_board=True)
    y = 20
    x = 20
    game.add(y, x, 'tower')
    game.validate()
    game.draw(debug_power=True, save="test/2")

    assert game.energy[y - 2, x - 9] == 0
    assert game.energy[y - 8, x] == 1
    assert game.energy[y - 8, x - 4] == 1
    assert game.energy[y - 8, x - 5] == 0
    assert game.energy[y - 7, x - 5] == 1
    assert game.energy[y - 6, x - 6] == 1
    assert game.energy[y - 7, x - 6] == 0
    assert game.energy[y - 6, x - 7] == 0


def test3():
    game = Game(empty_board=True)
    y = 20
    x = 7
    game.add(y, x, 'tower')
    game.validate()
    game.draw(debug_power=True, save="test/3")

    assert game.energy[y - 2, x + 9] == 0
    assert game.energy[y - 8, x] == 1
    assert game.energy[y - 8, x + 4] == 1
    assert game.energy[y - 8, x + 5] == 0
    assert game.energy[y - 7, x + 5] == 1
    assert game.energy[y - 6, x + 6] == 1
    assert game.energy[y - 7, x + 6] == 0
    assert game.energy[y - 6, x + 7] == 0


def test4():
    game = Game(empty_board=True)
    y = 7
    x = 20
    game.add(y, x, 'tower')
    game.validate()
    game.draw(debug_power=True, save="test/4")

    assert game.energy[y + 2, x - 9] == 0
    assert game.energy[y + 8, x] == 1
    assert game.energy[y + 8, x - 4] == 1
    assert game.energy[y + 8, x - 5] == 0
    assert game.energy[y + 7, x - 5] == 1
    assert game.energy[y + 6, x - 6] == 1
    assert game.energy[y + 7, x - 6] == 0
    assert game.energy[y + 6, x - 7] == 0
