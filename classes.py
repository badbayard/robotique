import enum
try:
    from typing import Union, Optional, List
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
        else:
            return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, tuple):
            return Position(self.x - other[0], self.y - other[1])
        else:
            return Position(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return 'Position({}, {})'.format(self._x, self._y)


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
            return self.board._explored[self.board._cell_index(self.pos)]

        @explored.setter
        def explored(self, e: bool):
            self.board._explored[self.board._cell_index(self.pos)] = e

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
                        [Wall.Yes] if strict else [Wall.Yes, Wall.Unknown]):
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

        self._explored = [False] * (self.reserved_height * self.reserved_width)
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
            return IndexError
        return self.Cell(self, key)


@enum.unique
class BoardColor(enum.Enum):
    Unknown = '?'
    Red = 'Red'
    Wood = 'Wood'
    Black = 'Black'
    White = 'White'

    @classmethod
    def from_itensity(cls, inten: int) -> 'BoardColor':
        if inten <= 20:
            return cls.Black
        elif 50 <= inten <= 65:
            return cls.Wood
        elif 70 <= inten <= 85:
            return cls.Red
        elif inten >= 90:
            return cls.White
        return cls.Unknown


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


class TerminalView:
    HorizontalWalls = {
        Wall.Unknown: '\x1B[2m─?─\x1B[22m',
        Wall.Yes: '━━━',
        Wall.No: '   '
    }
    VerticalWalls = {
        Wall.Unknown: '\x1B[2m?\x1B[22m',
        Wall.Yes: '┃',
        Wall.No: ' '
    }

    def __init__(self, board: Board, bot: Bot):
        # self.clear()
        self.board = board
        self.bot = bot

    def display(self):
        board = self.board
        bot = self.bot
        for y in range(board.min_y, board.max_y + 1):
            if y == board.min_y:
                print('┌' + self.HorizontalWalls[board[
                    Position(board.min_x, y)].wall(Direction.North)], end='')
                for x in range(board.min_x + 1, board.max_x + 1):
                    print('┬' + self.HorizontalWalls[board[
                        Position(x, y)].wall(Direction.North)], end='')
                print('┐', end='')
            else:
                print('├' + self.HorizontalWalls[board[
                    Position(board.min_x, y)].wall(Direction.North)], end='')
                for x in range(board.min_x + 1, board.max_x + 1):
                    print('┼' + self.HorizontalWalls[board[
                        Position(x, y)].wall(Direction.North)], end='')
                print('┤', end='')
            print('')
            for x in range(board.min_x, board.max_x + 1):
                char = '   '
                if x == bot.pos.x and y == bot.pos.y:
                    char = {
                        Direction.North: ' ↑ ',
                        Direction.East: ' → ',
                        Direction.South: ' ↓ ',
                        Direction.West: ' ← ',
                        Direction.Unknown: ' ? '
                    }[bot.dir]
                cell = board[Position(x, y)]
                color = ''  # if cell.explored else '\x1B[100m'
                if not cell.explored:
                    char = '\x1B[2m - '
                print(self.VerticalWalls[cell.wall(Direction.West)] + '{}{}\x1B[49m\x1B[22m'.format(color, char), end='')
            print(self.VerticalWalls[board[
                Position(board.max_x, y)].wall(Direction.East)])
        print('└' + self.HorizontalWalls[board[
            Position(board.min_x, board.max_y)].wall(Direction.South)], end='')
        for x in range(board.min_x + 1, board.max_x + 1):
            print('┴' + self.HorizontalWalls[board[
                Position(x, board.max_y)].wall(Direction.South)], end='')
        print('┘')

    @staticmethod
    def clear():
        print('\x1Bc', end='', flush=True)


if __name__ == '__main__':
    import time, sys

    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

    b = Board(3, 3)
    bot = Bot(b)
    tv = TerminalView(b, bot)
    b[Position(0, 0)].explored = True
    for x in range(len(b._walls)):
        b._walls[x] = Wall.Yes
        tv.display()
        time.sleep(0.3)
