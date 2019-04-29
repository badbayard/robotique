#! etc/bin/env python3
from ev3dev.ev3 import *
from time import sleep

def turn_left():
	mB = LargeMotor('outB')
	mC = LargeMotor('outC')
	mB.run_timed(time_sp=2750, speed_sp=-150)
	mC.run_timed(time_sp=2750, speed_sp=150)
                                                                             
                                                                               
                                                                               
                    
