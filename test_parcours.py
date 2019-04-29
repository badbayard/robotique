#! etc/bin/env python3
from ev3dev.ev3 import *
from time import sleep
from turn_left_color import turn_left
from turn_right_color import turn_right
from calibrage import calibrage
from test_forward import forward
import random

nb_de_tour = 30
current_tour = 0
continuer = True
autoDirection = True
turn = "left"
direction = -1

us2 = UltrasonicSensor('in2')
#us2.mode = 'US-DIST-CM'

us3 = UltrasonicSensor('in3')
#us3.mode = 'US-DIST-CM'

while(continuer):
	direction = forward(direction)
	#dist_left = us2.value()
	#dist_right = us3.value()	
	#print("gauche : ", us2.value())
	#print("droite : ", us3.value())
	#print("")
	#if(dist_left<=15):
	#	direction = turn_left(direction)
	#elif(dist_right<=15):
	#	direction = turn_right(direction)
	#else:
	#	print("firstTurn")
	#	direction = turn_left(direction)
	#	print("nextTurn")
	#	direction = turn_left(direction)
	if(random.randint(0,1) ==0):
		direction = turn_left(direction)
	else:
		direction = turn_right(direction)
	

	if(direction == 0):
		print("haut")
	if(direction == 1):
		print("droite")
	if(direction == 2):
		print("bas")
	if(direction == 3):
		print("gauche")

#	if(autoDirection):
#		if(not random.randint(0,1) == 0):
#			turn_right(direction)	
#		else:
#			turn_left(direction)
#	else:
#		if(turn == "left"):
#			turn_left()
#		else:
#			turn_right()	
#
#	current_tour = current_tour +1
#	print("continuer le parcours ? y or n")
#	mot = input()
#	if(mot == "n"):
#		continuer = False
#		autoDirection = True
#	if(mot == "c"):
#		autoDirection = False
#		print("left or right ?")
#		turn = input()
	

