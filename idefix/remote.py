from typing import Union

from idefix import Bot, Direction, RelativeDirection, Wall, Board
from idefix.realrobot import robot_json_entry
from socket import *
import sys


class RemoteBot(Bot):
    def __init__(self, hostname: str):
        conf = robot_json_entry(hostname)
        super().__init__(name=hostname, color=conf['color'])
        serverPort = 2000                   # use arbitrary port > 1024
        self.s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
        self.s.connect((conf['ip'], serverPort)) # connect to server on the port

    def wall(self, dir: Union[Direction, RelativeDirection]) -> Wall:
        if isinstance(dir, Direction):
            dir = self.dir.get_relative(dir)
        self.s.send(b'w '+dir.encode('utf-8'))
        raise NotImplementedError('wall')

    def stop(self, *args):
        self.s.send(b'stop')
        
    def direction(self, *args, **kwargs):
        d = ""
        self.s.send(b'd '+d.encode('utf-8'))
        raise NotImplementedError('direction')
               
    def forward(self, count: int = 1, *args, **kwargs) -> None:
        self.s.send(b'f')
        #raise NotImplementedError('forward')

    def turn_left(self, *args, **kwargs):
        self.s.send(b'l')
        #raise NotImplementedError('turn_left')

    def turn_right(self, *args, **kwargs):
        self.s.send(b'r')
        #raise NotImplementedError('turn_right')

    def write_info(self, board: Board, *args, **kwargs):
        raise NotImplementedError('write_info')
