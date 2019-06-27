from typing import Union

from idefix import Bot, Direction, RelativeDirection, Wall, Board
from idefix.realrobot import robot_json_entry
from socket import *


class RemoteBot(Bot):
    def __init__(self, hostname: str):
        conf = robot_json_entry(hostname)
        super().__init__(name=hostname, color=conf['color'],
                         skip_dir_init=True)
        serverPort = 2000                   # use arbitrary port > 1024
        self.s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
        self.s.connect((conf['ip'], serverPort)) # connect to server on the port
        self._dir = None

    @property
    def dir(self):
        if self._dir is None:
            self.s.send(b'd')
            dirmap = {
                b'n': Direction.North,
                b'e': Direction.East,
                b's': Direction.South,
                b'w': Direction.West,
                b'?': Direction.Unknown
            }
            self._dir = dirmap[self.s.recv(1)]
            assert self.s.recv(2) == b'OK'
        return self._dir

    @dir.setter
    def dir(self, d: Direction):
        dirmap = {
            Direction.North: b'n',
            Direction.East: b'e',
            Direction.South: b's',
            Direction.West: b'w'
        }
        self.s.send(b'd ' + dirmap[d])
        assert self.s.recv(2) == b'OK'
        self._dir = d

    def wall(self, dir: Union[Direction, RelativeDirection]) -> Wall:
        if isinstance(dir, Direction):
            dir = self.dir.get_relative(dir)
        self.s.send(b'w '+dir.encode('utf-8'))
        raise NotImplementedError('wall')

    def stop(self, *args):
        self.s.send(b'stop')
        assert self.s.recv(2) == b'OK'
               
    def forward(self, count: int = 1, *args, **kwargs) -> None:
        self.s.send(b'f')
        assert self.s.recv(2) == b'OK'

    def turn_left(self, *args, **kwargs):
        self.s.send(b'l')
        assert self.s.recv(2) == b'OK'

    def turn_right(self, *args, **kwargs):
        self.s.send(b'r')
        assert self.s.recv(2) == b'OK'

    def write_info(self, board: Board, *args, **kwargs):
        raise NotImplementedError('write_info')
