import collections
import enum
try:
    from typing import Union
except ImportError:
    pass


Position = collections.namedtuple('Position', 'x y')


@enum.unique
class RelativeDirection(enum.Enum):
    Front = 'F'
    Right = 'R'
    Back = 'B'
    Left = 'L'


@enum.unique
class Direction(enum.Enum):
    Unknown = '?'
    North = 'N'
    East = 'E'
    South = 'S'
    West = 'W'

    def apply_relative(self, rel: RelativeDirection):
        return {
            Direction.North: {
                RelativeDirection.Front: Direction.North,
                RelativeDirection.Right: Direction.East,
                RelativeDirection.Back: Direction.South,
                RelativeDirection.Left: Direction.West,
            },
            Direction.East: {
                RelativeDirection.Front: Direction.East,
                RelativeDirection.Right: Direction.South,
                RelativeDirection.Back: Direction.West,
                RelativeDirection.Left: Direction.North,
            },
            Direction.South: {
                RelativeDirection.Front: Direction.South,
                RelativeDirection.Right: Direction.West,
                RelativeDirection.Back: Direction.North,
                RelativeDirection.Left: Direction.East,
            },
            Direction.West: {
                RelativeDirection.Front: Direction.West,
                RelativeDirection.Right: Direction.North,
                RelativeDirection.Back: Direction.East,
                RelativeDirection.Left: Direction.South,
            }
        }.get(self, {}).get(rel, Direction.Unknown)


@enum.unique
class Wall(enum.Enum):
    Unknown = '?'
    Yes = '|'
    No = ' '


class Board:
    def __init__(self, max_width: int, max_height: int):
        self.max_width = max_width
        self.max_height = max_height

        self.reserved_height = max_height * 2 - 1
        self.reserved_width = max_width * 2 - 1

        self.explored = [[False] * self.reserved_height] * self.reserved_width
        self.walls = [Wall.Unknown] * (max_height * 2 + 1) * (max_width * 2 + 1)

    def explored(self, pos: Position) -> bool:
        return self.explored[pos.x][pos.y]

    def wall(self, pos: Position, dir: Direction) -> Wall:
        if dir in (Direction.West, Direction.East):
            idx = pos.x + pos.y * (self.reserved_width + 1)
            if dir == Direction.East:
                idx += 1
        else:
            offset = (self.reserved_width + 1) * self.reserved_height
            idx = offset + pos.y + pos.x * (self.reserved_width + 1)
            if dir == Direction.South:
                idx += 1
        return self.walls[idx]


class Bot:
    def __init__(self, board: Board):
        self.board = board
        self.pos = Position(0, 0)
        self.dir = Direction.Unknown

    def wall(self, dir):
        # type: (Union[Direction, RelativeDirection]) -> Wall
        if isinstance(dir, RelativeDirection):
            dir = self.dir.apply_relative(dir)
        return self.board.wall(self.pos, dir)
