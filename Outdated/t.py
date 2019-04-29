from ev3dev.ev3 import *
import ev3dev
import ev3dev.ev3 as ev3
from time import sleep

# Constantes

DISTANCE_COLLISION_CM = 10

# Sensors

colorSensor = ColorSensor('in4')
colorSensor.mode = 'COL-COLOR'
colors=('unknown','black','blue','green','yellow','red','white','brown')

mC = Motor("outC")
mD = Motor("outD")

us = UltrasonicSensor() 
# Put the US sensor into distance mode.
us.mode='US-DIST-CM'
units = us.units
# reports 'cm' even though the sensor measures 'mm'


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
        distance = us.value()/10  # convert mm to cm
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
# Main

def main():
    forward_until_obstacle()


if __name__ == '__main__':
    main()





    

