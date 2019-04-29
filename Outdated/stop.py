from ev3dev.ev3 import *
import ev3dev
import ev3dev.ev3 as ev3
from time import sleep

mC = Motor("outC")
mD = Motor("outD")

def motor_stop():
    mC.stop()
    mD.stop()

motor_stop()