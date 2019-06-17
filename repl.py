#!/usr/bin/env python3
from realrobot import *

class REPLCommand:
    def __init__(self, name: Optional[str] = None,
                 shorthand: Optional[str] = None, doc: Optional[str] = None):
        self.name = name or getattr(self, 'NAME')
        self.shorthand = shorthand or getattr(self, 'SHORTHAND')
        self.doc = doc or getattr(self, 'DOC', '')

    def __call__(self, bot: RealBot, *args, **kwargs):
        raise NotImplementedError


REPLCommandList = []  # type: List[REPLCommand]


def command(clazz):
    REPLCommandList.append(clazz())
    return clazz


@command
class HelpCommand(REPLCommand):
    NAME = 'help'
    SHORTHAND = '?'
    DOC = "Show this help"

    def __call__(self, bot: RealBot, *args, **kwargs):
        for cmdclass in REPLCommandList:
            print("{} - {}: {}".format(
                cmdclass.shorthand, cmdclass.name, cmdclass.doc))


@command
class ForwardCommand(REPLCommand):
    NAME = 'forward'
    SHORTHAND = 'f'

    def __call__(self, bot: RealBot, *args, **kwargs):
        bot.forward()


@command
class BackwardCommand(REPLCommand):
    NAME = 'backward'
    SHORTHAND = 'b'

    def __call__(self, bot: RealBot, *args, **kwargs):
        bot.backward()


@command
class LeftCommand(REPLCommand):
    NAME = 'left'
    SHORTHAND = 'l'

    def __call__(self, bot: RealBot, *args, **kwargs):
        try:
            bot.turn_left(pulses=int(args[0]))
        except IndexError:
            bot.turn_left()


@command
class RightCommand(REPLCommand):
    NAME = 'right'
    SHORTHAND = 'r'

    def __call__(self, bot: RealBot, *args, **kwargs):
        try:
            bot.turn_right(pulses=int(args[0]))
        except IndexError:
            bot.turn_right()


@command
class StopCommand(REPLCommand):
    NAME = 'stop'
    SHORTHAND = 'stop'

    def __call__(self, bot: RealBot, *args, **kwargs):
        bot.stop()


@command
class DirectionCommand(REPLCommand):
    NAME = 'direction'
    SHORTHAND = 'd'
    DOC = "Set or get direction"

    def __call__(self, bot: RealBot, *args, **kwargs):
        try:
            namemap = {
                'n': Direction.North,
                'r': Direction.East,
                's': Direction.South,
                'w': Direction.West
            }
            olddir = bot.dir
            bot.dir = namemap[args[0]]
            print("{} -> {}".format(olddir, bot.dir))
        except IndexError:
            print(bot.dir)


@command
class SequenceCommand(REPLCommand):
    NAME = 'sequence'
    SHORTHAND = 'seq'
    DOC = "Run no-args commands sequentially"

    def __call__(self, bot: RealBot, *args, **kwargs):
        seq = str(args[0])
        print(bot.dir)
        for instr in seq:
            repl_cmd(bot, instr)


@command
class SpeedCommand(REPLCommand):
    NAME = 'speed'
    SHORTHAND = 's'
    DOC = "Get or set robot speeds"

    def __call__(self, bot: RealBot, *args, **kwargs):
        if len(args) >= 2:
            bot.DEFAULT_SPEED = float(args[0])
            bot.DEFAULT_ROTATE_SPEED = float(args[1])
        print("DEFAULT_SPEED: {}\nDEFAULT_ROTATE_SPEED: {}".format(
            bot.DEFAULT_SPEED, bot.DEFAULT_ROTATE_SPEED))


import traceback
import readline  # Historique sur le input()


def repl_cmd(bot: RealBot, cmd: str, args: Optional[List] = None):
    try:
        cmdinst = [c for c in REPLCommandList if c.shorthand == cmd][0]
    except IndexError:
        print("Unknown command '{}'".format(cmd))
        return
    cmdinst(bot, *args if args is not None else [])


def repl(b: Board, bot: RealBot):
    import platform
    hostname = platform.node()
    prompt = "R!" + hostname + "> "
    del hostname
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
            repl_cmd(bot, cmd, args)
        except BaseException as e:
            print(traceback.format_exc())


if __name__ == '__main__':
    calib = get_robot_calibration(RobotColor.Green)
    b = Board(8, 8)
    bot = EV3Bot(calib, board=b)

    repl(b, bot)
    bot.stop()
