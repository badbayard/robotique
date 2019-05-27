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

Game = (grid[256],moves[256],robots[4],token,last)
Entry = (key,depth)
Set = (mask,size)

def swap(array, a , b):
    temp = array[a]
    array[a] = array[b]
    array[b] = temp

def make_key():
    global Game