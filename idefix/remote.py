from typing import Union

from idefix import Bot, Direction, RelativeDirection, Wall, Board
from idefix.realrobot import robot_json_entry
from socket import *


class RemoteBot(Bot):
    DIRNAMEMAP = {
        Direction.North: b'n',
        Direction.East: b'e',
        Direction.South: b's',
        Direction.West: b'w',
        RelativeDirection.Front: b'f',
        RelativeDirection.Right: b'r',
        RelativeDirection.Back: b'b',
        RelativeDirection.Left: b'l'
    }

    def __init__(self, hostname: str):
        conf = robot_json_entry(hostname)
        super().__init__(name=hostname, color=conf['color'],
                         skip_dir_init=True)
        serverPort = 2000                   # use arbitrary port > 1024
        self.s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
        self.s.connect((conf['ip'], serverPort)) # connect to server on the port
        self.s.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
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
        self.s.send(b'd ' + self.DIRNAMEMAP[d])
        assert self.s.recv(2) == b'OK'
        self._dir = d

    def wall(self, dir: Union[Direction, RelativeDirection]) -> Wall:
        self.s.send(b'w ' + self.DIRNAMEMAP[dir])
        wall = Wall(self.s.recv(1).decode('ascii'))
        assert self.s.recv(2) == b'OK'
        return wall

    def stop(self):
        self.s.send(b'stop')
        assert self.s.recv(2) == b'OK'
               
    def forward(self, count: int = 1, *args, **kwargs) -> None:
        self.s.send(b'f ' + bytes(str(count), 'ascii'))
        assert self.s.recv(2) == b'OK'

    def turn_left(self, *args, **kwargs):
        self.s.send(b'l')
        assert self.s.recv(2) == b'OK'

    def turn_right(self, *args, **kwargs):
        self.s.send(b'r')
        assert self.s.recv(2) == b'OK'

    def write_info(self, board: Board, *args, **kwargs):
        raise NotImplementedError('write_info')
