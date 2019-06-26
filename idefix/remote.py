from typing import Union

from idefix import Bot, Direction, RelativeDirection, Wall, Board
from idefix.realrobot import robot_json_entry


class RemoteBot(Bot):
    def __init__(self, hostname: str):
        conf = robot_json_entry(hostname)
        super().__init__(name=hostname, color=conf['color'])

    def wall(self, dir: Union[Direction, RelativeDirection]) -> Wall:
        raise NotImplementedError('wall')

    def forward(self, count: int = 1, *args, **kwargs) -> None:
        raise NotImplementedError('forward')

    def turn_left(self, *args, **kwargs):
        raise NotImplementedError('turn_left')

    def turn_right(self, *args, **kwargs):
        raise NotImplementedError('turn_right')

    def write_info(self, board: Board, *args, **kwargs):
        raise NotImplementedError('write_info')
