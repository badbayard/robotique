#! etc/bin/env python3
from ev3dev.ev3 import *
from time import sleep

m = LargeMotor('outC')
m.run_timed(time_sp=9900, speed_sp=300)
m2 = LargeMotor('outB')
m2.run_timed(time_sp=9900, speed_sp=300)


