#! etc/bin/env python3
from ev3dev.ev3 import *
from time import sleep

def forward():
	m = LargeMotor('outC')
	m2 = LargeMotor('outB')
	m.run_timed(time_sp=3250, speed_sp=300)
	m2.run_timed(time_sp=3250, speed_sp=300)



