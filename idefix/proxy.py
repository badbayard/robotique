import enum
from typing import Union, Optional, List

from idefix import Bot, Direction, RelativeDirection, Wall, Board


@enum.unique
class Command(enum.Enum):
    Forward = 0,
    TurnLeft = 1,
    TurnRight = 2,
    Wall = 3,
    WriteInfo = 4


class Instruction:
    __slots__ = ['bot', 'command', 'args']

    def __init__(self, bot: Bot, command: Command, args: Optional[List] = None):
        self.bot = bot
        self.command = command
        self.args = args

    def to_json_dict(self):
        json = {
            'bot': self.bot.name,
            'cmd': self.command.name
        }
        if self.args is not None:
            json['args'] = self.args
        return json

    def __repr__(self):
        return "Instruction(" + repr(self.to_json_dict()) + ")"


class ProxyBot(Bot):
    def __init__(self, bot: Bot):
        super().__init__(skip_init=True)
        self.bot = bot
        self.command_list = []  # type: List[Instruction]

    def clear_command_list(self):
        self.command_list = []

    def _cmd(self, cmd: Command, args: Optional[List] = None):
        self.command_list.append(Instruction(self.bot, cmd, args))

    @property
    def pos(self):
        return self.bot.pos

    @pos.setter
    def pos(self, pos):
        self.bot.pos = pos

    @property
    def dir(self):
        return self.bot.dir

    @dir.setter
    def dir(self, dir):
        self.bot.dir = dir

    @property
    def color(self):
        return self.bot.color

    @property
    def name(self):
        return self.bot.name

    def wall(self, dir: Union[Direction, RelativeDirection]) -> Wall:
        self._cmd(Command.Wall, [dir.value])
        return self.bot.wall(dir)

    def forward(self, count: int = 1, *args, **kwargs) -> None:
        self._cmd(Command.Forward, [count])
        return self.bot.forward(count, *args, **kwargs)

    def turn_left(self, *args, **kwargs):
        self._cmd(Command.TurnLeft)
        return self.bot.turn_left(*args, **kwargs)

    def turn_right(self, *args, **kwargs):
        self._cmd(Command.TurnRight)
        return self.bot.turn_right(*args, **kwargs)

    def write_info(self, board: Board, *args, **kwargs):
        self._cmd(Command.WriteInfo)
        return self.bot.write_info(board, *args, **kwargs)

    def __repr__(self):
        return "ProxyBot('{}')".format(self.bot.name)
