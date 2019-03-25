#!/etc/bin/env python3
#o that script can be run from Brickman

from ev3dev.ev3 import * 
from time import sleep

mB = LargeMotor('outB')
mC = LargeMotor('outC')

mB.stop()
mC.stop()
