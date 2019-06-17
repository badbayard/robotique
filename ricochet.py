from ev3dev.ev3 import *
import ev3dev.ev3 as ev3
from time import sleep
from typing import Callable

NORTH = 0x01
EAST = 0x02
SOUTH = 0X04
WEST = 0x08
ROBOT = 0X10

REVERSE = [0 , SOUTH, WEST,0,NORTH,0,0,0,EAST]
OFFSET = [0,-16,1,0,16,0,0,0,-1]

#Game = (grid[256],moves[256],robots[1],token,last)
# Entry = (key,depth)
# Set = (mask,size)
#
MAX_DEPTH = 32


def HAS_WALL(x, wall):
    return x & wall


def HAS_ROBOT(x):
    return x & ROBOT


def PACK_MOVE(robot, direction):
    return robot << 4 | direction


def PACK_UNDO(robot, start, last): \
    return robot << 16 | start << 8 | last


def UNPACK_ROBOT(undo):
    return (undo >> 16) & 0xff


def UNPACK_START(undo):
    return (undo >> 8) & 0xff


def UNPACK_LAST(undo):
    return undo & 0xff


class Game:
    def __init__(self):
        self.grid = [0] * 64
        self.moves = [0] * 64
        self.robots = [0] * 3
        self.token = 0
        self.last = 0


class Entry:
    def __init__(self, Nkey=0, Ndepth=0):
        self.key = Nkey
        self.depth = Ndepth


class Set:
    def __init__(self):
        self.mask = 0
        self.size = 0


def swap(array, a , b):
    temp = array[a]
    array[a] = array[b]
    array[b] = temp


def MAKE_KEY(x):
    x = (x[0] | (x[1] << 8) | (x[2]<< 16) )


def make_key():
    global Game
    robots = [0] * 3
    if robots[1] > robots[2]:
        swap(robots,1,2)
    return MAKE_KEY(robots)


def hash(key: int) -> int:
    key = ~key + (key << 15)
    key = key ^ (key >> 12)
    key = key + (key << 2)
    key = key ^ (key >> 4)
    key = key * 2057
    key = key ^ (key >> 16)
    return key


def game_over(game: Game) -> bool:
    if game.robots[0] == game.token:
        return True

    else:
        return False


def can_move(game: Game, robot: int, direction: int) -> bool:
    index = game.robots[robot]
    if HAS_WALL(game.grid[index], direction):
        return False

    if game.last == PACK_MOVE(robot, REVERSE[direction]):
        return False

    new_index = index + OFFSET[direction]
    if HAS_ROBOT(game.grid[new_index]):
        return False

    return True


def compute_move(game: Game,robot: int, direction: int) ->int :
    index = game.robots[robot] + OFFSET[direction]
    while True:
        if HAS_WALL(game.grid[index], direction):
            break

        new_index = index + OFFSET[direction]
        if HAS_ROBOT(game.grid[new_index]):
            break

        index = new_index

    return index


def do_move(game: Game, robot: int, direction: int) -> int:
    start = game.robots[robot]
    end = compute_move(game, robot, direction)
    last = game.last
    game.robots[robot] = end
    game.last = PACK_MOVE(robot, direction)
    game.grid[start] &= ~ROBOT
    game.grid[end] |= ROBOT
    return PACK_UNDO(robot, start, last)


def undo_move (game: Game, undo: int):
    robot = UNPACK_ROBOT(undo)
    start = UNPACK_START(undo)
    last = UNPACK_LAST(undo)
    end = game.robots[robot]
    game.robots[robot] = start
    game.last = last
    game.grid[start] |= ROBOT
    game.grid[end] &= ~ROBOT


def precompute_minimum_moves(game: Game):
    status = [False] * 64
    game.move = [0xffffffff] * 64

    game.moves[game.token] = 0
    status[game.token] = True
    done = False
    while not done:
        done = True
        for i  in range(64):
            if not status[i]:
                continue

            status[i] = False
            depth = game.moves[i] + 1
            for direction in range(1, 8):
                index = i
                while not HAS_WALL(game.grid[index], direction):
                    if game.moves[index] > depth:
                        game.moves[index] = depth
                        status[index] = True
                        done = False


_nodes = 0
_hits = 0
_inner = 0


def _search(game: Game, depth: int, max_depth: int, path: chr):
    global _nodes
    _nodes += 1
    if game_over(game):
        return depth

    if depth == max_depth:
        return 0

    height = max_depth - depth
    if game.moves[game.robots[0]] > height:
        return 0

    # if height != 1 and not set_add(set, make_key(game), height):
    #     global _hits
    #     _hits += 1
    #     return 0

    global _inner
    _inner += 1
    for robot in range(4):
        if robot and game.moves[game.robots[0]] == height:
            continue

        for direction in range(1, 8):
            if not can_move(game, robot, direction):
                continue

            undo = do_move(game, robot, direction)
            result = _search(
                game, depth + 1, max_depth, path
            )
            undo_move(game, undo)
            if result:
                path[depth] = PACK_MOVE(robot, direction)
                return result
    return 0


#j'ai ommis tous les appel à Set (préexistant en python)
def search(game: Game, path: chr, callback: Callable[[int, int, int, int], None]):
    if game_over(game):
        return 0
    result = 0
    precompute_minimum_moves(game)
    for max_depth in range(1, MAX_DEPTH):
        global _nodes
        global _hits
        global _inner
        _nodes = 0
        _hits = 0
        _inner = 0
        result = _search(game, 0, max_depth, path)
        if callback:
            callback(max_depth, _nodes, _inner, _hits)
        if result:
            break
    return result


def _callback(depth, nodes, inner,  hits):
    print (depth, nodes, inner, hits)


if __name__ == "__main__":
    game = Game()
    game.robots = [196, 197, 135]
    game.token = 54
    path = [] * 32
    search(game, path, _callback)
