from ev3dev.ev3 import *
from time import sleep

m = LargeMotor("outC")
m.run_forever(speed=450)

