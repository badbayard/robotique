import random

from idefix import Board, Wall, Direction, Position


def randwall(wall_chance: float):
    return random.choices([Wall.Yes, Wall.No], [wall_chance, 1-wall_chance])[0]


def generate_board(max_width: int, max_height: int, wall_chance: float = 0.2) \
        -> Board:
    board = Board(max_width, max_height)
    xoffset = random.randint(-max_width + 1, 0)
    yoffset = random.randint(-max_height + 1, 0)
    yrange = range(0 + yoffset, board.max_y + 1 + yoffset)
    xrange = range(0 + xoffset, board.max_x + 1 + xoffset)
    for y in yrange:
        for x in xrange:
            cell = board[Position(x, y)]
            cell.explored = True
            cell.set_wall(
                Direction.North,
                Wall.Yes if y == yrange.start else randwall(wall_chance))
            cell.set_wall(
                Direction.South,
                Wall.Yes if y == yrange.stop-1 else randwall(wall_chance))
            cell.set_wall(
                Direction.East,
                Wall.Yes if x == xrange.stop-1 else randwall(wall_chance))
            cell.set_wall(
                Direction.West,
                Wall.Yes if x == xrange.start else randwall(wall_chance))

    return board
