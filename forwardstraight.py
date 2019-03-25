#! etc/bin/env python3
from ev3dev.ev3 import *
import ev3dev
import ev3dev.ev3 as ev3
from time import sleep
# Constantes

DISTANCE_COLLISION_CM = 6
VITESSE_BASE = 300

# Sensors

colorSensor = ColorSensor('in4')
colorSensor.mode = 'COL-COLOR'
colors=('unknown','black','blue','green','yellow','red','white','brown')


us = UltrasonicSensor('in1') 
# Put the US sensor into distance mode.
us.mode='US-DIST-CM'
units = us.units

mB = LargeMotor('outB')
mC = LargeMotor('outC')

mB.run_forever(speed_sp=VITESSE_BASE)
mC.run_forever(speed_sp=VITESSE_BASE)

stop = False
redORwhite = False
while not stop:
	distance = us.value()/10  # convert mm to cm
	print(distance)
	stop=(distance < DISTANCE_COLLISION_CM)
	couleur = colors[colorSensor.value()]
	if (couleur == "black"):
		mB.run_forever(speed_sp=VITESSE_BASE)
		mC.run_forever(speed_sp=VITESSE_BASE)
		redORwhite = False
	elif (couleur == "white" or couleur== "red"):
		mB.run_forever(speed_sp=VITESSE_BASE+70)
		mC.run_forever(speed_sp=VITESSE_BASE-70)
		redORwhite = True
	elif couleur=="brown":
		if not(redORwhite):
			mB.run_forever(speed_sp=VITESSE_BASE-70)
			mC.run_forever(speed_sp=VITESSE_BASE+70)
	
	else:
		stop=True
		print(couleur)

mB.stop()
mC.stop()
