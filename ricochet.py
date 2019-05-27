from ev3dev.ev3 import *
import ev3dev.ev3 as ev3
from time import sleep

NORTH = 0x01
EAST = 0x02
SOUTH = 0X04
WEST = 0x08
ROBOT = 0X10

REVERSE = [0 , SOUTH, WESTR,0,NORTH,0,0,0,EAST]
OFFSET = [0,-16,1,0,16,0,0,0,-1]

# Game = (grid[256],moves[256],robots[4],token,last)
# Entry = (key,depth)
# Set = (mask,size)


class Game:
    def __init__(self):
        self.grid = [0] * 256
        self.robots = [0] * 4
        self.token = 0
        self.last = 0


class Entry:
    def __init__(self):
        self.key = 0
        self.depth = 0

    def __init__(self,Nkey,Ndepth):
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


def make_key():
    global Game
    robots = [0] * 4


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
        return true;

    else:
        return false;


def can_move(game: Game, robot: int, direction: int) -> bool:
    index = game.robots[robot]
    if HAS_WALL(game.grid[index], direction):
        return false;

    if game.last == PACK_MOVE(robot, REVERSE[direction]):
        return false;

    new_index = index + OFFSET[direction]
    if HAS_ROBOT(game.grid[new_index]):
        return false

    return true
