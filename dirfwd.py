#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep, time
from classes import BoardColor, Direction, RelativeDirection

# Constantes

DISTANCE_COLLISION_CM = 6
VITESSE_BASE = 500

# Sensors

colorSensor = ColorSensor('in4')
colorSensor.mode = 'COL-REFLECT'

fwdSensor = UltrasonicSensor('in1')
fwdSensor.mode = 'US-DIST-CM'
leftSensor = UltrasonicSensor('in2')
leftSensor.mode = 'US-DIST-CM'
rightSensor = UltrasonicSensor('in3')
rightSensor.mode = 'US-DIST-CM'

mB = LargeMotor('outB')
mC = LargeMotor('outC')


print("Detection direction cardinale:")

print("- Bande de couleur... ", end='')
sens = 1
mB.run_forever(speed_sp=-140*sens)
mC.run_forever(speed_sp=140*sens)
while True:
    color = BoardColor.from_itensity(colorSensor.reflected_light_intensity)
    if color not in (BoardColor.Unknown, BoardColor.Wood):
        break
    sleep(0.05)

first_color = color
print(str(first_color))

print("- Detection 2eme bande... ", end='')
sens = -1
mB.run_forever(speed_sp=-70*sens)
mC.run_forever(speed_sp=70*sens)
while True:
    color = BoardColor.from_itensity(colorSensor.reflected_light_intensity)
    if color != first_color and color != BoardColor.Unknown:
        break
    sleep(0.05)
sens = 1
mB.run_forever(speed_sp=-70*sens)
mC.run_forever(speed_sp=70*sens)
while True:
    color = BoardColor.from_itensity(colorSensor.reflected_light_intensity)
    if color == first_color:
        break
    sleep(0.05)
while True:
    color = BoardColor.from_itensity(colorSensor.reflected_light_intensity)
    if color != first_color and color not in (BoardColor.Unknown, BoardColor.Wood):
        break
    sleep(0.05)

mB.stop()
mC.stop()

second_color = color
print(str(second_color))

# Map de couleurs directionelles pour une rotation antihoraire
dirmap = {
    (BoardColor.Black, BoardColor.Red): Direction.North,
    (BoardColor.White, BoardColor.Black): Direction.East,
    (BoardColor.Red, BoardColor.Black): Direction.South,
    (BoardColor.Black, BoardColor.White): Direction.West
}
direction = dirmap[(first_color, second_color)]

print("Direction: " + str(direction))

colmap = {
    Direction.North: (BoardColor.Red, BoardColor.Black),
    Direction.East: (BoardColor.Black, BoardColor.White),
    Direction.South: (BoardColor.Black, BoardColor.Red),
    Direction.West: (BoardColor.White, BoardColor.Black)
}

stop = False
sens = 1
colleft = ""
rotate_clockwise = None

try:
    rolltime = sys.argv[1]
except (KeyError, IndexError):
    rolltime = 2
while True:
    start = time()
    while True:
        sleep(0.1)
        distance = fwdSensor.value() / 10  # convert mm to cm
        print(distance)
        stop = distance < DISTANCE_COLLISION_CM
        couleur = BoardColor.from_itensity(colorSensor.reflected_light_intensity)
        print(couleur)

        if colorSensor.reflected_light_intensity == 0 or stop:
            mB.stop()
            mC.stop()
            continue

        if couleur == colmap[direction][1]:
            rotate_clockwise = False
            mB.run_forever(speed_sp=VITESSE_BASE+(-70*sens))
            mC.run_forever(speed_sp=VITESSE_BASE+(70*sens))
        elif couleur == colmap[direction][0]:
            rotate_clockwise = True
            mB.run_forever(speed_sp=VITESSE_BASE+(70*sens))
            mC.run_forever(speed_sp=VITESSE_BASE+(-70*sens))
        elif couleur == BoardColor.Wood:
            if rotate_clockwise:
                mB.run_forever(speed_sp=(70 * sens))
                mC.run_forever(speed_sp=(-70 * sens))
            else:
                mB.run_forever(speed_sp=(-70 * sens))
                mC.run_forever(speed_sp=(70 * sens))

        if time() - start > rolltime:
            break
    mB.stop()
    mC.stop()
    rotate_clockwise = True
    mB.run_forever(speed_sp=-140 * (-1 if rotate_clockwise else 1))
    mC.run_forever(speed_sp=140 * (-1 if rotate_clockwise else 1))
    while True:
        color = BoardColor.from_itensity(colorSensor.reflected_light_intensity)
        if color == BoardColor.Wood:
            break
        sleep(0.05)
    while True:
        color = BoardColor.from_itensity(colorSensor.reflected_light_intensity)
        if color != BoardColor.Wood:
            break
        sleep(0.05)
    direction = direction.apply_relative(RelativeDirection.Left)




mB.stop()
mC.stop()
