import enum
from abc import ABC, abstractmethod
from typing import Union, Optional, List, Tuple, Dict, Any


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
        else:
            return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, tuple):
            return Position(self.x - other[0], self.y - other[1])
        else:
            return Position(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return 'Position({}, {})'.format(self._x, self._y)

    def __lt__(self, other):
        if isinstance(other, Position):
            if self._x < other._x:
                return True
            return self._y < other._y
        return False

    def __eq__(self, other):
        if isinstance(other, Position):
            return self._x == other._x and self._y == other._y
        return False

    def __hash__(self):
        return hash((self._x, self._y))

    def move(self, dir: 'Direction') -> 'Position':
        delta = {
            Direction.North: (0, -1),
            Direction.East: (1, 0),
            Direction.South: (0, 1),
            Direction.West: (-1, 0)
        }.get(dir)
        return Position(self._x + delta[0], self._y + delta[1])

    def get_direction_to(self, pos: 'Position') -> 'Direction':
        return {
            (0, -1): Direction.North,
            (1, 0): Direction.East,
            (0, 1): Direction.South,
            (-1, 0): Direction.West
        }[(pos._x - self._x, pos._y - self._y)]

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

    def get_relative(self, dir: 'Direction') -> RelativeDirection:
        return {
            Direction.North: {
                Direction.North: RelativeDirection.Front,
                Direction.East: RelativeDirection.Right,
                Direction.South: RelativeDirection.Back,
                Direction.West: RelativeDirection.Left
            },
            Direction.East: {
                Direction.North: RelativeDirection.Left,
                Direction.East: RelativeDirection.Front,
                Direction.South: RelativeDirection.Right,
                Direction.West: RelativeDirection.Back
            },
            Direction.South: {
                Direction.North: RelativeDirection.Back,
                Direction.East: RelativeDirection.Left,
                Direction.South: RelativeDirection.Front,
                Direction.West: RelativeDirection.Right
            },
            Direction.West: {
                Direction.North: RelativeDirection.Right,
                Direction.East: RelativeDirection.Back,
                Direction.South: RelativeDirection.Left,
                Direction.West: RelativeDirection.Front
            }
        }.get(self, {}).get(dir, None)

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
            return self.board._explored[self.board._cell_index(self.pos)]

        @explored.setter
        def explored(self, e: bool):
            self.board._explored[self.board._cell_index(self.pos)] = e

        @property
        def explored_by(self) -> Optional['Bot']:
            return self.board._data[self.board._cell_index(self.pos)].get(
                'explored_by', None)

        @explored_by.setter
        def explored_by(self, b):
            self.board._data[self.board._cell_index(self.pos)]['explored_by'] \
                = b

        @property
        def data(self) -> Dict[str, Any]:
            return self.board._data[self.board._cell_index(self.pos)]

        def wall(self, dir: Direction) -> Wall:
            return self.board._walls[self.board._wall_index(self.pos, dir)]

        def set_wall(self, dir: Direction, wall: Wall):
            self.board._walls[self.board._wall_index(self.pos, dir)] = wall

        def neighbour(self, dir):
            # type: (Direction) -> Optional['Cell']
            try:
                return self.board[self.pos + {
                    Direction.North: (0, -1),
                    Direction.East: (1, 0),
                    Direction.South: (0, 1),
                    Direction.West: (-1, 0)
                }[dir]]
            except IndexError:
                return None

        @property
        def accessible_neighbours(self, strict=False):
            # type: (bool) -> List['Cell']
            acc = []
            for dir in [Direction.North, Direction.East,
                        Direction.South, Direction.West]:
                if self.wall(dir) in (
                        [Wall.No] if strict else [Wall.No, Wall.Unknown]):
                    neigh = self.neighbour(dir)
                    if neigh is not None:
                        acc.append(neigh)
            return acc

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

        self.min_x = -max_width + 1
        self.min_y = -max_height + 1
        self.min_pos = Position(self.min_x, self.min_y)
        self.max_x = max_width - 1
        self.max_y = max_height - 1
        self.max_pos = Position(self.max_x, self.max_y)

        cellcount = self.reserved_height * self.reserved_width
        self._explored = [False] * cellcount
        self._data = []
        for _ in range(cellcount):
            self._data.append({})
        self._walls = [Wall.Unknown] * (
                (self.reserved_width + 1) * self.reserved_height +
                (self.reserved_height + 1) * self.reserved_width
        )

    def _cell_index(self, pos: Position) -> int:
        x = pos.x - self.min_x
        y = pos.y - self.min_y
        return x + y * self.reserved_width

    def _wall_index(self, pos: Position, dir: Direction) -> int:
        x = pos.x - self.min_x
        y = pos.y - self.min_y
        if dir in (Direction.West, Direction.East):
            idx = x + y * (self.reserved_width + 1)
            if dir == Direction.East:
                idx += 1
        else:
            offset = (self.reserved_width + 1) * self.reserved_height
            idx = offset + y + x * (self.reserved_width + 1)
            if dir == Direction.South:
                idx += 1
        return idx

    def __getitem__(self, key: Position):
        if not (self.min_x <= key.x <= self.max_x) or \
           not (self.min_y <= key.y <= self.max_y):
            raise IndexError
        return self.Cell(self, key)

    def __contains__(self, pos: Position):
        return self.min_x <= pos.x <= self.max_x and \
               self.min_y <= pos.y <= self.max_y


BoardColorCalibration = List[Tuple[Tuple[int, int], 'BoardColor']]


@enum.unique
class BoardColor(enum.Enum):
    Unknown = '?'
    Red = 'Red'
    Wood = 'Wood'
    Black = 'Black'
    White = 'White'

    @classmethod
    def from_itensity(cls, inten: int, cal: BoardColorCalibration) \
            -> 'BoardColor':
        for centry in cal:
            if centry[0][0] <= inten <= centry[0][1]:
                return centry[1]
        return cls.Unknown


DirectionColorMap = {
    Direction.North: (BoardColor.Red, BoardColor.Black),
    Direction.East: (BoardColor.Black, BoardColor.White),
    Direction.South: (BoardColor.Black, BoardColor.Red),
    Direction.West: (BoardColor.White, BoardColor.Black)
}


ColorDirectionMap = {
    (BoardColor.Red, BoardColor.Black): Direction.North,
    (BoardColor.Black, BoardColor.White): Direction.East,
    (BoardColor.Black, BoardColor.Red): Direction.South,
    (BoardColor.White, BoardColor.Black): Direction.West
}


class Bot(ABC):
    def __init__(self, name: str = "red", color: Optional[List[int]] = None,
                 skip_init: bool = False):
        if not skip_init:
            self.pos = Position(0, 0)
            self.dir = Direction.Unknown
            self.color = color or [255, 0, 0]
            self.name = name

    @property
    def dir_front(self):
        return self.dir

    @property
    def dir_back(self):
        return self.dir.apply_relative(RelativeDirection.Back)

    @property
    def dir_left(self):
        return self.dir.apply_relative(RelativeDirection.Left)

    @property
    def dir_right(self):
        return self.dir.apply_relative(RelativeDirection.Right)

    @abstractmethod
    def wall(self, dir: Union[Direction, RelativeDirection]) -> Wall:
        ...

    @abstractmethod
    def forward(self, count: int = 1, *args, **kwargs) -> None:
        ...

    @abstractmethod
    def turn_left(self, *args, **kwargs):
        ...

    @abstractmethod
    def turn_right(self, *args, **kwargs):
        ...

    @abstractmethod
    def write_info(self, board: Board, *args, **kwargs):
        ...


class RealWorldError(RuntimeError):
    pass


class FakeBot(Bot):
    def __init__(self, board: Board, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board

    def wall(self, dir: Union[Direction, RelativeDirection]) -> Wall:
        if isinstance(dir, RelativeDirection):
            dir = self.dir.apply_relative(dir)
        return self.board[self.pos].wall(dir)

    def forward(self, count: int = 1, *args, **kwargs) -> None:
        for _ in range(count):
            if self.board[self.pos].wall(self.dir) != Wall.No:
                raise RealWorldError("Ran into a wall")
            nextpos = self.pos.move(self.dir)
            if nextpos not in self.board:
                raise ValueError("Moved too far")
            self.pos = nextpos

    def turn_left(self, *args, **kwargs):
        self.dir = self.dir.apply_relative(RelativeDirection.Left)

    def turn_right(self, *args, **kwargs):
        self.dir = self.dir.apply_relative(RelativeDirection.Right)

    def write_info(self, board: Board, *args, **kwargs):
        cell = board[self.pos]
        ocell = self.board[self.pos]
        cell.set_wall(self.dir_left, ocell.wall(self.dir_left))
        cell.set_wall(self.dir, ocell.wall(self.dir))
        cell.set_wall(self.dir_right, ocell.wall(self.dir_right))
        cell.explored = True
        cell.explored_by = self
