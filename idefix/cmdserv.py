#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Optional, List, Union
import traceback
import platform
import readline  # Historique sur le input()
from socket import *
import sys
from idefix import Board, Direction, RelativeDirection
from idefix.realrobot import RealBot, EV3Bot, get_robot_calibration


class CmdServContext:
    __slots__ = ['board', 'bot', 'conn']

    def __init__(self, board: Board, bot: RealBot, conn: socket):
        self.board = board
        self.bot = bot
        self.conn = conn

    def send(self, data: Union[bytes, str]):
        if isinstance(data, str):
            print('< ' + data)
            self.conn.send(data.encode('utf-8'))
        else:
            print('< ' + data.decode('utf-8'))
            self.conn.send(data)


class CmdServCommand(ABC):
    def __init__(self, name: Optional[str] = None,
                 shorthand: Optional[str] = None, doc: Optional[str] = None):
        self.name = name or getattr(self, 'NAME')
        self.shorthand = shorthand or getattr(self, 'SHORTHAND')
        self.doc = doc or getattr(self, 'DOC', '')

    @abstractmethod
    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        ...


CmdServCommandList = []  # type: List[CmdServCommand]


def command(clazz):
    CmdServCommandList.append(clazz())
    return clazz


@command
class HelpCommand(CmdServCommand):
    NAME = 'help'
    SHORTHAND = b'?'
    DOC = "Show this help"

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        for cmdclass in CmdServCommandList:
            print("{} - {}: {}".format(
                cmdclass.shorthand, cmdclass.name, cmdclass.doc))


@command
class ForwardCommand(CmdServCommand):
    NAME = 'forward'
    SHORTHAND = b'f'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        if len(args) == 1:
            ctx.bot.forward(int(args[0]))
        else:
            ctx.bot.forward()


@command
class BackwardCommand(CmdServCommand):
    NAME = 'backward'
    SHORTHAND = b'b'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        ctx.bot.backward()


@command
class LeftCommand(CmdServCommand):
    NAME = 'left'
    SHORTHAND = b'l'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        try:
            ctx.bot.turn_left(pulses=int(args[0]))
        except IndexError:
            ctx.bot.turn_left()


@command
class RightCommand(CmdServCommand):
    NAME = 'right'
    SHORTHAND = b'r'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        try:
            ctx.bot.turn_right(pulses=int(args[0]))
        except IndexError:
            ctx.bot.turn_right()


@command
class WallCommand(CmdServCommand):
    NAME = 'wall'
    SHORTHAND = b'w'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        dirmap = {
            b'n': Direction.North,
            b'e': Direction.East,
            b's': Direction.South,
            b'w': Direction.West,
            b'f': RelativeDirection.Front,
            b'r': RelativeDirection.Right,
            b'b': RelativeDirection.Back,
            b'l': RelativeDirection.Left
        }
        ctx.send(ctx.bot.wall(dirmap[args[0]]).value)


@command
class StopCommand(CmdServCommand):
    NAME = 'stop'
    SHORTHAND = b'stop'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        ctx.bot.stop()


@command
class DirectionCommand(CmdServCommand):
    NAME = 'direction'
    SHORTHAND = b'd'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        try:
            namemap = {
                b'n': Direction.North,
                b'e': Direction.East,
                b's': Direction.South,
                b'w': Direction.West,
                b'?': Direction.Unknown
            }
            olddir = ctx.bot.dir
            ctx.bot.dir = namemap[args[0]]
            print("{} -> {}".format(olddir, ctx.bot.dir))
        except IndexError:
            print(ctx.bot.dir)
            dirmap = {
                Direction.North: b'n',
                Direction.East: b'e',
                Direction.South: b's',
                Direction.West: b'w',
                Direction.Unknown: b'?'
            }
            ctx.send(dirmap[ctx.bot.dir])


@command
class SequenceCommand(CmdServCommand):
    NAME = 'sequence'
    SHORTHAND = b'seq'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        seq = str(args[0])
        print(ctx.bot.dir)
        for instr in seq:
            repl_cmd(ctx, instr)


@command
class SpeedCommand(CmdServCommand):
    NAME = 'speed'
    SHORTHAND = b's'

    def __call__(self, ctx: CmdServContext, *args, **kwargs):
        if len(args) >= 2:
            ctx.bot.DEFAULT_SPEED = float(args[0])
            ctx.bot.DEFAULT_ROTATE_SPEED = float(args[1])
        print("DEFAULT_SPEED: {}\nDEFAULT_ROTATE_SPEED: {}".format(
            ctx.bot.DEFAULT_SPEED, ctx.bot.DEFAULT_ROTATE_SPEED))


def repl_cmd(ctx: CmdServContext, cmd: bytes, args: Optional[List] = None):
    try:
        cmdinst = [c for c in CmdServCommandList if c.shorthand == cmd][0]
    except IndexError:
        print("Unknown command '{}'".format(cmd))
        return
    cmdinst(ctx, *args if args is not None else [])


def repl(ctx: CmdServContext):
    while True:
        cmd_raw = ctx.conn.recv(1024)
        print('< ' + cmd_raw.decode('utf-8'))
        cmd_raw = cmd_raw.split(b' ')
        cmd = cmd_raw[0]
        args = cmd_raw[1:]
        del cmd_raw
        try:
            repl_cmd(ctx, cmd, args)
        except BaseException as e:
            print(traceback.format_exc())
        ctx.send(b'OK')


if __name__ == '__main__':
    b = Board(8, 8)
    bot = EV3Bot(platform.node(), board=b)

    hostname = platform.node()
    myPort = 2000
    print(hostname, myPort)
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', myPort))
    s.listen(1)

    while True:
        try:
            connection, address = s.accept()  # connection is a new socket
            connection.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
            repl(CmdServContext(b, bot, connection))
        except BrokenPipeError:
            print("Broken pipe!")
            pass

    bot.stop()
