from idefix import *
from typing import List


class TerminalBoardView:
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

    def __init__(self, board: Board, bots: List[Bot]):
        # self.clear()
        self.board = board
        self.bots = bots

    def display(self):
        board = self.board
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
                for bot in self.bots:
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
                print(self.VerticalWalls[cell.wall(Direction.West)] +
                      '{}{}\x1B[49m\x1B[22m'.format(color, char), end='')
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
    bot = FakeBot(b)
    tv = TerminalBoardView(b, [bot])
    b[Position(0, 0)].explored = True
    for x in range(len(b._walls)):
        b._walls[x] = Wall.Yes
        tv.display()
        time.sleep(0.3)
