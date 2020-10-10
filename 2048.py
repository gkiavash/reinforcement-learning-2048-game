from functools import reduce, partial
from itertools import count, groupby, starmap


def compose(*funcs):
    return reduce(lambda a, e: lambda x: a(e(x)), funcs, lambda x: x)


# base = int(input("Choose a base. (2 for normal 2048)\n> "))
base = 2


def addn(board):
    from random import randrange, sample

    inds = range(base ** 2)
    empties = [(y, x) for y in inds for x in inds if not board[y][x]]
    for y, x in sample(empties, 2 ** (base - 2)):
        board[y][x] = base if randrange(10) else base ** 2
    return board


def squish(row):
    r = []
    for n, x in starmap(lambda n, a: (n, sum(map(bool, a))),
                        groupby(filter(bool, row))):
        r += ([n * base] * (x // base)) + ([n] * (x % base))
    return r + ([None] * (base ** 2 - len(r)))


def myprint(board):
    for i in board:
        print(i)


def transpose(l): return [list(x) for x in zip(*l)]


flip = partial(map, reversed)
thunk = compose(list, partial(map, list))

moveLeft = compose(thunk, partial(map, squish), thunk)
moveRight = compose(thunk, flip, moveLeft, flip)
moveUp = compose(transpose, moveLeft, transpose)
moveDown = compose(transpose, moveRight, transpose)

moves = {1: moveRight,
         2: moveLeft,
         3: moveUp,
         4: moveDown}

size = max(11 - base * 2, 3)  # box width

board = addn([[None for _ in range(base ** 2)] for _ in range(base ** 2)])
myprint(board)

while True:
    my_move = int(input("next move: "))
    moved = moves[my_move](board)
    if sum(not n for r in moved for n in r) < 2 ** (base - 2):
        break
    if moved != board:
        board = addn(moved)
    myprint(board)
