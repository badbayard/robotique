#! etc/bin/env python3
from ev3dev.ev3 import *
import ev3dev
import ev3dev.ev3 as ev3
from time import sleep
# Constantes

DISTANCE_COLLISION_CM = 6

# Sensors

colorSensor = ColorSensor('in4')
colorSensor.mode = 'COL-COLOR'
colors=('unknown','black','blue','green','yellow','red','white','brown')


us = UltrasonicSensor('in1')
usG = UltrasonicSensor('in2')
usD = UltrasonicSensor('in3')
# Put the US sensor into distance mode.
us.mode = 'US-DIST-CM'
usG.mode = 'US-DIST-CM'
usD.mode = 'US-DIST-CM'
units = us.units

def detectionFace():
	distance = us.value() / 10  # convert mm to cm
	# print("distance " + str(distance))
	return distance < DISTANCE_COLLISION_CM

def detectionGauche():
	distanceG = usG.value()  # convert mm to cm
	# print("distance G" + str(distanceG))
	return distanceG < DISTANCE_COLLISION_CM

def detectionDroit():
	distanceD = usD.value()  # convert mm to cm
	# print("distance D" + str(distanceD))
	return distanceD < DISTANCE_COLLISION_CM

stop=False
while not stop:
	stop = detectionGauche() or detectionFace() or detectionDroit()

	couleur = colors[colorSensor.value()]
