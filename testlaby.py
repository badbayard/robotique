#! etc/bin/env python3

from forward import forward
from time import sleep
i=0
while(i<7):
	forward()
	sleep(3)	
	i=i+1	
