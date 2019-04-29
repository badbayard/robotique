#! etc/bin/env python3
from ev3dev.ev3 import *
import ev3dev.ev3 as ev3
from time import sleep
# Constantes
def turn_left(direction):
	VITESSE_BASE = 300

# Sensors

	colorSensor = ColorSensor('in4')
	colorSensor.mode = 'COL-COLOR'
	colors=('unknown','black','blue','green','yellow','red','white','brown')


	mB = LargeMotor('outB')
	mC = LargeMotor('outC')

	mB.run_forever(speed_sp=-VITESSE_BASE)
	mC.run_forever(speed_sp=VITESSE_BASE)

	stop = False
	onBrown= False
	couleur = ""
	nbOfBrown = 0
	nbColor = 0
	while not stop:
		couleur = colors[colorSensor.value()]
		if (onBrown == True and (couleur  == "red" or couleur == "blue" or couleur =="black" or couleur == "white")):
			nbColor = nbColor + 1
			if(nbColor > 20):
				stop = True
				print(nbOfBrown)
				print(nbColor)
		if(couleur == "brown"):
			nbOfBrown = nbOfBrown +1
			if(nbOfBrown >=150):
				onBrown = True

	mB.stop()
	mC.stop()
	if(direction == 0):
		return 3	
	else:
		return direction - 1
