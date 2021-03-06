#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Optional, List
import traceback
import platform
import sys
import readline  # Historique sur le input()

from idefix import Board, Direction, Bot, RelativeDirection


class REPLContext:
    __slots__ = ['board', 'bot']

    def __init__(self, board: Board, bot: Bot):
        self.board = board
        self.bot = bot


class REPLCommand(ABC):
    def __init__(self, name: Optional[str] = None,
                 shorthand: Optional[str] = None, doc: Optional[str] = None):
        self.name = name or getattr(self, 'NAME')
        self.shorthand = shorthand or getattr(self, 'SHORTHAND')
        self.doc = doc or getattr(self, 'DOC', '')

    @abstractmethod
    def __call__(self, ctx: REPLContext, *args, **kwargs):
        ...


REPLCommandList = []  # type: List[REPLCommand]


def command(clazz):
    REPLCommandList.append(clazz())
    return clazz


@command
class HelpCommand(REPLCommand):
    NAME = 'help'
    SHORTHAND = '?'
    DOC = "Show this help"

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        for cmdclass in REPLCommandList:
            print("{} - {}: {}".format(
                cmdclass.shorthand, cmdclass.name, cmdclass.doc))


@command
class ForwardCommand(REPLCommand):
    NAME = 'forward'
    SHORTHAND = 'f'

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        if len(args) == 1:
            ctx.bot.forward(int(args[0]))
        else:
            ctx.bot.forward()


@command
class BackwardCommand(REPLCommand):
    NAME = 'backward'
    SHORTHAND = 'b'

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        ctx.bot.backward()


@command
class LeftCommand(REPLCommand):
    NAME = 'left'
    SHORTHAND = 'l'

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        try:
            ctx.bot.turn_left(pulses=int(args[0]))
        except IndexError:
            ctx.bot.turn_left()


@command
class RightCommand(REPLCommand):
    NAME = 'right'
    SHORTHAND = 'r'

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        try:
            ctx.bot.turn_right(pulses=int(args[0]))
        except IndexError:
            ctx.bot.turn_right()


@command
class WallCommand(REPLCommand):
    NAME = 'wall'
    SHORTHAND = 'w'

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        namemap = {
            'n': Direction.North,
            'e': Direction.East,
            's': Direction.South,
            'w': Direction.West,
            'f': RelativeDirection.Front,
            'r': RelativeDirection.Right,
            'b': RelativeDirection.Back,
            'l': RelativeDirection.Left
        }
        print(ctx.bot.wall(namemap[args[0]]))


@command
class WallCommand(REPLCommand):
    NAME = 'all_walls'
    SHORTHAND = 'w*'

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        board = Board(8, 8)
        ctx.bot.write_info(board)
        walls = ''
        walls += board[ctx.bot.pos].wall(Direction.North).value
        walls += board[ctx.bot.pos].wall(Direction.East).value
        walls += board[ctx.bot.pos].wall(Direction.South).value
        walls += board[ctx.bot.pos].wall(Direction.West).value
        print(walls)


@command
class StopCommand(REPLCommand):
    NAME = 'stop'
    SHORTHAND = 'stop'

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        ctx.bot.stop()


@command
class DirectionCommand(REPLCommand):
    NAME = 'direction'
    SHORTHAND = 'd'
    DOC = "Set or get direction"

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        try:
            namemap = {
                'n': Direction.North,
                'e': Direction.East,
                's': Direction.South,
                'w': Direction.West,
                'o': Direction.West
            }
            olddir = ctx.bot.dir
            ctx.bot.dir = namemap[args[0]]
            print("{} -> {}".format(olddir, ctx.bot.dir))
        except IndexError:
            print(ctx.bot.dir)


@command
class EmergencyStopCommand(REPLCommand):
    NAME = 'emerstop'
    SHORTHAND = 'es'
    DOC = "Enale or disable emergency stop"

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        ctx.bot.emergency_stop(args[0] == '1')


@command
class SequenceCommand(REPLCommand):
    NAME = 'sequence'
    SHORTHAND = 'seq'
    DOC = "Run no-args commands sequentially"

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        seq = str(args[0])
        print(ctx.bot.dir)
        for instr in seq:
            repl_cmd(ctx, instr)


@command
class SpeedCommand(REPLCommand):
    NAME = 'speed'
    SHORTHAND = 's'
    DOC = "Get or set robot speeds"

    def __call__(self, ctx: REPLContext, *args, **kwargs):
        if len(args) >= 2:
            ctx.bot.DEFAULT_SPEED = float(args[0])
            ctx.bot.DEFAULT_ROTATE_SPEED = float(args[1])
        print("DEFAULT_SPEED: {}\nDEFAULT_ROTATE_SPEED: {}".format(
            ctx.bot.DEFAULT_SPEED, ctx.bot.DEFAULT_ROTATE_SPEED))


def repl_cmd(ctx: REPLContext, cmd: str, args: Optional[List] = None):
    try:
        cmdinst = [c for c in REPLCommandList if c.shorthand == cmd][0]
    except IndexError:
        print("Unknown command '{}'".format(cmd))
        return
    cmdinst(ctx, *args if args is not None else [])


def repl(ctx: REPLContext, display_hostname: str):
    prompt = "R!" + display_hostname + "> "
    print("Use '?' to get help")
    while True:
        try:
            cmd_raw = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("quit")
            break
        cmd_raw = cmd_raw.split(' ')
        cmd = cmd_raw[0]
        args = cmd_raw[1:]
        del cmd_raw
        try:
            repl_cmd(ctx, cmd, args)
        except BaseException as e:
            print(traceback.format_exc())


if __name__ == '__main__':
    b = Board(8, 8)
    if len(sys.argv) > 1:
        from idefix.remote import RemoteBot
        hostname = sys.argv[1]
        bot = RemoteBot(hostname)
        display_hostname = "@" + hostname
    else:
        from idefix.realrobot import EV3Bot
        bot = EV3Bot(platform.node(), board=b)
        display_hostname = platform.node()
    repl(REPLContext(b, bot), display_hostname)
    bot.stop()
