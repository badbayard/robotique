from typing import Union, Optional

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
        print("Connected to " + hostname)
        self._dir = None  # type: Optional[Direction]

    def send(self, data: bytes):
        print("{: 4}> {}".format(len(data), data.decode()))
        self.s.send(data)

    def recv(self, buffer_size: int):
        print("{: 4}< ".format(buffer_size), end='')
        buf = self.s.recv(buffer_size)
        print(buf.decode())
        return buf

    @property
    def dir(self):
        if self._dir is None:
            self.send(b'd')
            dirmap = {
                b'n': Direction.North,
                b'e': Direction.East,
                b's': Direction.South,
                b'w': Direction.West,
                b'?': Direction.Unknown
            }
            self._dir = dirmap[self.s.recv(1)]
            assert self.recv(2) == b'OK'
        return self._dir

    @dir.setter
    def dir(self, d: Direction):
        self.send(b'd ' + self.DIRNAMEMAP[d])
        assert self.recv(2) == b'OK'
        self._dir = d

    def wall(self, dir: Union[Direction, RelativeDirection]) -> Wall:
        self.send(b'w ' + self.DIRNAMEMAP[dir])
        wall = Wall(self.recv(1).decode('ascii'))
        assert self.recv(2) == b'OK'
        return wall

    def stop(self):
        self.send(b'stop')
        assert self.recv(2) == b'OK'
               
    def forward(self, count: int = 1, *args, **kwargs) -> None:
        self.send(b'f ' + bytes(str(count), 'ascii'))
        assert self.recv(2) == b'OK'
        for _ in range(count):
            self.pos = self.pos.move(self._dir)

    def turn_left(self, *args, **kwargs):
        self.send(b'l')
        assert self.recv(2) == b'OK'
        self._dir = self._dir.apply_relative(RelativeDirection.Left)

    def turn_right(self, *args, **kwargs):
        self.send(b'r')
        assert self.recv(2) == b'OK'
        self._dir = self._dir.apply_relative(RelativeDirection.Right)

    def write_info(self, board: Board, *args, **kwargs):
        cell = board[self.pos]
        self.send(b'w*')
        walls_bytes = self.recv(4)
        assert self.recv(2) == b'OK'
        walls = walls_bytes.decode()
        if walls[0] != Wall.Unknown.value:
            cell.set_wall(Direction.North, Wall(walls[0]))
        if walls[1] != Wall.Unknown.value:
            cell.set_wall(Direction.East, Wall(walls[1]))
        if walls[2] != Wall.Unknown.value:
            cell.set_wall(Direction.South, Wall(walls[2]))
        if walls[3] != Wall.Unknown.value:
            cell.set_wall(Direction.West, Wall(walls[3]))
        cell.explored = True
        cell.explored_by = self

    def emergency_stop(self, enable: bool):
        self.send(b'es 1' if enable else b'es 0')
        assert self.recv(2) == b'OK'
