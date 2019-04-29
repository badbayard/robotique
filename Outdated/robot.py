#! etc/bin/env python3
from ev3dev.ev3 import *
from time import sleep


class Robot():

    def __init__(self):
        self.vitesse=300
        self.motorG='outB'
        self.motorD='outC'
        self.distance=5
        self.capteurDist='in1'
        self.capteurCoul='in4'
        
