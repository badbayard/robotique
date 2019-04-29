#! etc/bin/env python3
from ev3dev.ev3 import *
import ev3dev.ev3 as ev3
from time import sleep
# Constantes
def calibrage():
	VITESSE_BASE = 50

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
	while not stop:
		couleur = colors[colorSensor.value()]
		if(couleur == "brown"):
			nbOfBrown = nbOfBrown +1
			if(nbOfBrown >=150):
				stop = True
	mB.stop()
	mC.stop()
	mB.run_forever(speed_sp=VITESSE_BASE)
	mC.run_forever(speed_sp=-VITESSE_BASE)

	stop = False

	nbColor = [0,0,0,0] #Nb of Red, nb of White , nb of Black, nb of Brown	
	tabColor = ["red","white","black","brown"]
	firstColor = -1
	while not stop:
		couleur = colors[colorSensor.value()]
		if(couleur == "brown" and (nbColor[0]!=0 or nbColor[1]!=0 or nbColor[2]!=0)):
			nbColor[3] = nbColor[3] + 1
		if(couleur == "white"):
			nbColor[1] = nbColor[1] + 1
		if(couleur =="black"):
			nbColor[2] = nbColor[2] + 1
		if(couleur == "red"):
			nbColor[0] = nbColor[0] + 1
		if(nbColor[3] > 149):
			stop = True
		if(firstColor == -1):
			if(nbColor[0]>100):
				firstColor = 0
			if(nbColor[1]>100):
				firstColor = 1
			if(nbColor[2]>100):
				firstColor = 2
	secondColor = -1
	tmp = 0
	for i in nbColor :
		if(i>150 and tmp != firstColor and tabColor[tmp]!="brown"):
			secondColor = tmp
		tmp = tmp + 1

	print("firstColor : " + tabColor[firstColor])
	print("secondColor : " + tabColor[secondColor])

	mB.stop()
	mC.stop()
	
	stop = False
	mB.run_forever(speed_sp=-VITESSE_BASE)
	mC.run_forever(speed_sp=VITESSE_BASE)
	nbFirstColor = 0
	while not stop:
		couleur = colors[colorSensor.value()]
		if(couleur == tabColor[firstColor]):
 			nbFirstColor = nbFirstColor + 1
		if(nbFirstColor > 10):
			stop = True
	


	
	if(tabColor[firstColor] == "black"):
		if(tabColor[secondColor] == "white"):
			return 3
		else:
			return 0
	else :
		if(tabColor[firstColor] =="white" ):
			return 1
		else :
			return 2
