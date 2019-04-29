#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep

# Constantes

DISTANCE_COLLISION_CM = 10

# Global

# fenetre glissante non initialisee de taille 9 impair pour eviter conflit
fenGlissante = [-1] * 9


# Sensors

colorSensor = ColorSensor("in4")
colorSensor.mode = 'COL-COLOR'
colors=('unknown','black','blue','green','yellow','red','white','brown')

mC = Motor("outC")
mD = Motor("outD")

us1 = UltrasonicSensor("in1")
us2 = UltrasonicSensor("in2")
us3 = UltrasonicSensor("in3") 
# Put the US sensor into distance mode.
us1.mode='US-DIST-CM'
us2.mode='US-DIST-CM'
us3.mode='US-DIST-CM'
units = us1.units
# ev3 sensor report mm --> might div by 10
# older sensor report cm, but are less accurate



# Functions

def right_turn():
    motor_run_forever(mC,-200,mD,200)

def left_turn():
    motor_run_forever(mC,200,mD,-200)

def forward(speed):
    motor_run_forever(mC,speed,mD,speed)

def motor_stop():
    mC.stop()
    mD.stop()

def motor_run_forever(motor1, speed1, motor2, speed2):
    motor1.run_forever(speed_sp=speed1)
    motor2.run_forever(speed_sp=speed2)


def color_led():
    Leds.set_color(Leds.LEFT, Leds.RED)

def forward_until_obstacle():
   turn = False
   nbTurn = 0
   while nbTurn < 4:
        # US sensor will measure distance to the closest
        # object in front of it.
        distance = us1.value()/10  # convert mm to cm
        print(str(distance) + " " + units)

        if distance < DISTANCE_COLLISION_CM:
            right_turn()
            turn = True
        else:
            if turn:
                turn = False
                nbTurn += 1
            forward(400)

def turn_accordint_to_color():
    while True:
        couleur = colors[colorSensor.value()]
        print(couleur)
        sleep(1)

        if couleur == "black":
            forward(500)
        elif couleur == "blue":
            right_turn()
        elif couleur=="red":
            left_turn()
        else:
            motor_stop()
			
def check_color():
	couleur = colors[colorSensor.value()]
	return couleur
			
def check_average_color():
	global fenGlissante
	
	# unknown and other
	unknown = 0 
	black = 0
	red = 0
	white = 0
	brown = 0
	
	# remove first value and shift the other
	for i in range(8):
		fenGlissante[i] = fenGlissante[i+1]
		if fenGlissante[i] == "black":
			black += 1
		elif fenGlissante[i] == "red":
			red += 1
		elif fenGlissante[i] == "white":
			white += 1
		elif fenGlissante[i] == "brown":
			brown += 1
		else:
			unknown += 1
			
	# update last value
	fenGlissante[8] = check_color()
	
	if fenGlissante[8] == "black":
		black += 1
	elif fenGlissante[8] == "red":
		red += 1
	elif fenGlissante[8] == "white":
		white += 1
	elif fenGlissante[8] == "brown":
		brown += 1
	else:
		unknown += 1
			
	# sort the at the end the most dectected color
	lastIsBigger = sorted([unknown, black, red, white, brown])
	
	if lastIsBigger[4] == black:
		return "black"
	elif lastIsBigger[4] == red:
		return "red"
	elif lastIsBigger[4] == white:
		return "white"
	elif lastIsBigger[4] == brown:
		return "brown"
		
	return "unknown"
	
	
	
def test_color_turn():
	global fenGlissante
	while True:
		check_average_color()
		
			
# Main

def main():
	global fenGlissante
	for i in range(9):
		fenGlissante[i] = check_color()
	test_color_turn()


if __name__ == '__main__':
    main()





    

