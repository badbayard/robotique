#! etc/bin/env python3
from turn_left import turn_left
from forward import forward
from time import sleep
i=0
while(i<3):
        forward()
        sleep(4)
        i=i+1

turn_left()
sleep(4)
forward()
sleep(4)
forward()
sleep(4)
turn_left()
sleep(4)
i=0
while(i<3):
        forward()
        sleep(4)
        i=i+1


