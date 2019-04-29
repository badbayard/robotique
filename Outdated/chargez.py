#! etc/bin/env python3
from ev3dev.ev3 import *
from time import sleep


mB = LargeMotor('outB')
mC = LargeMotor('outC')
mB.run_forever(speed_sp=1000)
mC.run_forever(speed_sp=1000)



