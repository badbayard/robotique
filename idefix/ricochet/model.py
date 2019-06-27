from typing import List

from idefix import Board, Bot, Position, Direction, Wall

# Directions
NORTH = 'N'
EAST = 'E'
SOUTH = 'S'
WEST = 'W'

REVERSE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}

OFFSET = {
    NORTH: -16,
    EAST: 1,
    SOUTH: 16,
    WEST: -1,
}

# Masks
M_NORTH = 0x01
M_EAST  = 0x02
M_SOUTH = 0x04
M_WEST  = 0x08
M_ROBOT = 0x10

M_LOOKUP = {
    Direction.North: M_NORTH,
    Direction.East: M_EAST,
    Direction.South: M_SOUTH,
    Direction.West: M_WEST,
}


# Helper Functions
def idx(board: Board, pos: Position, size: int = 16):
    return (pos.y - board.min_y) * size + (pos.x - board.min_x)


def to_mask(cell: Board.Cell):
    result = 0
    for dir, mask in M_LOOKUP.items():
        if cell.wall(dir) == Wall.Yes:
            result |= mask
    return result


# Game
class Game:
    def __init__(self, board: Board, bots: List[Bot], destination: Position,
                 destbot: Bot):
        self.board = board
        self.bots = bots
        self.destination = destination
        self.destbot = destbot

    def robot_for_letter(self, letter: str) -> Bot:
        if letter == 'R':
            return self.bots[0]
        if letter == 'G':
            return self.bots[1]
        if letter == 'B':
            return self.bots[2]
        raise KeyError

    @staticmethod
    def direction_for_letter(letter: str) -> Direction:
        return {
            'N': Direction.North,
            'E': Direction.East,
            'S': Direction.South,
            'W': Direction.West
        }[letter]

    def export(self):
        token = idx(self.board, self.destination)
        robots = [idx(self.board, bot.pos) for bot in self.bots]
        grid = [0] * (16 * 16)
        for y in range(self.board.min_y, self.board.max_y + 1):
            for x in range(self.board.min_x, self.board.max_x + 1):
                pos = Position(x, y)
                cell = self.board[pos]
                gidx = idx(self.board, pos)
                grid[gidx] = to_mask(cell)
                for bot in self.bots:
                    if bot.pos == pos:
                        grid[gidx] |= M_ROBOT
        robot = self.bots.index(self.destbot)
        return {
            'grid': grid,
            'robot': robot,
            'token': token,
            'robots': robots,
        }
