from typing import Union

from idefix import Bot, Direction, RelativeDirection, Wall, Board


class ProxyBot(Bot):
    def __init__(self, bot: Bot):
        super().__init__(skip_init=True)
        self.bot = bot
        self.command_list = []

    def clear_command_list(self):
        self.command_list = []

    def _cmd(self, cmd: str):
        self.command_list.append({'bot': self.name, 'cmd': cmd})

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
        self._cmd('wall:' + dir.value)
        return self.bot.wall(dir)

    def forward(self, count: int = 1, *args, **kwargs) -> None:
        self._cmd('forward:' + str(count))
        return self.bot.forward(count, *args, **kwargs)

    def turn_left(self, *args, **kwargs):
        self._cmd('turn_left')
        return self.bot.turn_left(*args, **kwargs)

    def turn_right(self, *args, **kwargs):
        self._cmd('turn_right')
        return self.bot.turn_right(*args, **kwargs)

    def write_info(self, board: Board, *args, **kwargs):
        self._cmd('write_info')
        return self.bot.write_info(board, *args, **kwargs)

    def __repr__(self):
        return "ProxyBot('{}')".format(self.bot.name)
