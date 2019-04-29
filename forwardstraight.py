#! etc/bin/env python3
from ev3dev.ev3 import *
import ev3dev
import ev3dev.ev3 as ev3
from time import sleep
from collections import deque
# Constantes

DISTANCE_COLLISION_CM = 6
VITESSE_BASE = 300

# Sensors

colorSensor = ColorSensor('in4')
colorSensor.mode = 'COL-COLOR'
#colorSensor.mode = 'RAW-RGB'
colors=('unknown','black','blue','green','yellow','red','white','brown')
colWindow = deque(maxlen=5)
lastCol = 0
while True:
        colWindow.append(colorSensor.value())
        newCol = colors[max(set(colWindow), key=colWindow.count)]
        if newCol != lastCol:
                lastCol=newCol
                print(newCol)

us = UltrasonicSensor('in1') 
# Put the US sensor into distance mode.
us.mode='US-DIST-CM'
units = us.units

mB = LargeMotor('outB')
mC = LargeMotor('outC')


stop = False
sens=0
colleft =""

print("1")
print(colors[colorSensor.value()])
while (colors[colorSensor.value()]!="brown"):
        mB.run_forever(speed_sp=-50)
        mC.run_forever(speed_sp=50)
mB.stop()
mC.stop()
print("2")
print(colors[colorSensor.value()])
while (colors[colorSensor.value()]=="brown"):
        mB.run_forever(speed_sp=50)
        mC.run_forever(speed_sp=-50)
mB.stop()
mC.stop()
print("3")
print(colors[colorSensor.value()])
sleep(1)
colleft=colors[colorSensor.value()]
while (colors[colorSensor.value()]==colleft):
        mB.run_forever(speed_sp=50)
        mC.run_forever(speed_sp=-50)
mB.stop()
mC.stop()
print("4")
print(colors[colorSensor.value()])

if(colleft=="black"):
        sens=1
else:
        sens=-1
mB.run_forever(speed_sp=VITESSE_BASE)
mC.run_forever(speed_sp=VITESSE_BASE)

print("5")
print(colors[colorSensor.value()])
while not stop:
	distance = us.value()/10  # convert mm to cm
	print(distance)
	stop=(distance < DISTANCE_COLLISION_CM)
	couleur = colors[colorSensor.value()]
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
	
	else:
		stop=True
		print(couleur)

mB.stop()
mC.stop()
