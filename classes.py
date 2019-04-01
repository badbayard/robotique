import enum
try:
    from typing import Union, Optional
except ImportError:
    pass


class Position:
    __slot__ = ['_x', '_y']

    def __init__(self, *args):
        if isinstance(args[0], tuple):
            self._x = args[0][0]
            self._y = args[0][1]
        elif isinstance(args[0], Position):
            self._x = args[0].x
            self._y = args[0].y
        elif isinstance(args[0], int):
            self._x = args[0]
            self._y = args[1]
        else:
            raise ValueError

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __add__(self, other):
        if isinstance(other, tuple):
            return Position(self.x + other[0], self.y + other[1])
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, tuple):
            return Position(self.x - other[0], self.y - other[1])
        return Position(self.x - other.x, self.y - other.y)


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
    class Cell:
        def __init__(self, board: 'Board', pos: Position):
            self.board = board
            self.pos = pos

        @property
        def explored(self) -> bool:
            return self.board._explored[self.pos.x][self.pos.y]

        @explored.setter
        def explored(self, e: bool):
            self.board._explored[self.pos.x][self.pos.y] = e

        def wall(self, dir: Direction) -> Wall:
            return self.board._walls[self.board._wall_index(self.pos, dir)]

        def set_wall(self, dir: Direction, wall: Wall):
            self.board._walls[self.board._wall_index(self.pos, dir)] = wall

        def neighbour(self, dir):
            # type: (Direction) -> Optional[Cell]
            # TODO

        def __str__(self):
            walls = ''.join([
                self.wall(d).value for d in
                [Direction.North, Direction.East,
                 Direction.South, Direction.West]])
            return "Cell({}, {}, explored={}, walls={})".format(
                self.pos.x, self.pos.y, self.explored, walls)

    def __init__(self, max_width: int, max_height: int):
        self.max_width = max_width
        self.max_height = max_height

        self.reserved_height = max_height * 2 - 1
        self.reserved_width = max_width * 2 - 1

        self._explored = [[False] * self.reserved_height] * self.reserved_width
        self._walls = [Wall.Unknown] * (max_height * 2 + 1) * (max_width * 2 + 1)

    def _wall_index(self, pos: Position, dir: Direction) -> int:
        if dir in (Direction.West, Direction.East):
            idx = pos.x + pos.y * (self.reserved_width + 1)
            if dir == Direction.East:
                idx += 1
        else:
            offset = (self.reserved_width + 1) * self.reserved_height
            idx = offset + pos.y + pos.x * (self.reserved_width + 1)
            if dir == Direction.South:
                idx += 1
        return idx

    def __getitem__(self, key: Position):
        return self.Cell(self, key)


class Bot:
    def __init__(self, board: Board):
        self.board = board
        self.pos = Position(0, 0)
        self.dir = Direction.Unknown

    def wall(self, dir):
        # type: (Union[Direction, RelativeDirection]) -> Wall
        if isinstance(dir, RelativeDirection):
            dir = self.dir.apply_relative(dir)
        return self.board[self.pos].wall(dir)

