#! etc/bin/env python3
from turn_left import turn_left
from forward import forward

while(
instru= str(input("R for Right, L for Left, F for forward"))
print(instru)
if(instru=="R"):
	#turn_right()
	print("Not Implemented")
elif(instru=="L"):
	turn_left()
elif(instru=="F"):
	forward()

