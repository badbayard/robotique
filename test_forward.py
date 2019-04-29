#! etc/bin/env python3
from ev3dev.ev3 import *
import ev3dev
import ev3dev.ev3 as ev3
from time import sleep
from calibrage import calibrage
from collections import deque
# Constantes

def forward(direction):

	DISTANCE_COLLISION_CM = 6
	VITESSE_BASE = 200

	#set_sensor_mode('in2','other-uart')
	#port.mode = 'other-uart'
	# Sensors

	colorSensor = ColorSensor('in4')
	colorSensor.mode = 'COL-COLOR'
	#colorSensor.mode = 'RAW-RGB'
	colors=('unknown','black','blue','green','yellow','red','white','brown')
	#p = getPort("S1")
	us = UltrasonicSensor('in1') 
	us2 = UltrasonicSensor('in2')
	us2.isEnabled() 
	#us2.close()
	us3 = UltrasonicSensor('in3') 
	#us3.mode = 'other-uart'
	# Put the US sensor into distance mode.
	us.mode='US-DIST-CM'
	units = us.units

	mB = LargeMotor('outB')
	mC = LargeMotor('outC')


	stop = False
	if(direction == -1):
		direction = calibrage()
		if(direction == 0 or direction == 3):
			sens = -1
		else:
			sens = 1
	else:
		if(direction == 0 or direction ==3):
			sens = -1
		else:
			sens = 1
	mB.run_forever(speed_sp=VITESSE_BASE)
	mC.run_forever(speed_sp=VITESSE_BASE)

	print("5")
	print(colors[colorSensor.value()])
	while not stop:
		distance = us.value()/10  # convert mm to cm
		stop=(distance < DISTANCE_COLLISION_CM)
		couleur = colors[colorSensor.value()]
		print(distance)
		if (couleur == "black"):
			mB.run_forever(speed_sp=VITESSE_BASE+(-70*sens))
			mC.run_forever(speed_sp=VITESSE_BASE+(70*sens))
		elif (couleur == "white" or couleur== "red"):
			mB.run_forever(speed_sp=VITESSE_BASE+(70*sens))
			mC.run_forever(speed_sp=VITESSE_BASE+(-70*sens))
	#elif couleur=="brown":
	#	if not(redORwhite):
	#		mB.run_forever(speed_sp=VITESSE_BASE-70)
	#		mC.run_forever(speed_sp=VITESSE_BASE+70)
	
	#else:
	#	stop=True
	#	print(couleur)

	mB.stop()
	mC.stop()
	return direction
