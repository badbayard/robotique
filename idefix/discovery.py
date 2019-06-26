from typing import List

from idefix import Wall, Direction, Board, Position, RelativeDirection, astar
from idefix.proxy import ProxyBot


def run(board: Board, bot: ProxyBot):
    # On tourne pour savoir l'état des 4 murs autour du robot
    def mark_candidates(candidates):
        for cell in candidates:
            if Wall.No in (
                    cell.wall(Direction.North), cell.wall(Direction.East),
                    cell.wall(Direction.South), cell.wall(Direction.West)):
                cell.data['bgcolor'] = [255, 255, 128]

    def get_candidates() -> List[Board.Cell]:
        ret = []
        for y in range(board.min_y, board.max_y + 1):
            for x in range(board.min_x, board.max_x + 1):
                cell = board[Position(x, y)]
                if cell.explored:
                    continue
                if Wall.No in (
                        cell.wall(Direction.North), cell.wall(Direction.East),
                        cell.wall(Direction.South), cell.wall(Direction.West)):
                    ret.append(cell)
        return ret
    bot.write_info(board)
    mark_candidates(get_candidates())
    yield bot.command_list
    bot.clear_command_list()
    bot.turn_left()

    while True:
        bot.write_info(board)
        candidates = get_candidates()
        if len(candidates) == 0:
            break
        mark_candidates(candidates)

        candidates_paths = [*map(
            lambda d: astar.path(board, bot.pos, d.pos), candidates)]
        shortest_idx = min(enumerate(candidates_paths),
                           key=lambda x: len(x[1]))[0]

        candidates[shortest_idx].data['bgcolor'] = [255, 255, 0]

        yield bot.command_list
        bot.clear_command_list()

        path = candidates_paths[shortest_idx]
        nextpos = path[1]  # type: Position
        nextdir = None
        for d in (Direction.North, Direction.East,
                  Direction.South, Direction.West):
            if nextpos == bot.pos.move(d):
                nextdir = d
        reldir = bot.dir.get_relative(nextdir)
        if reldir == RelativeDirection.Front:
            bot.forward()
        elif reldir == RelativeDirection.Right:
            bot.turn_right()
        elif reldir == RelativeDirection.Back:
            bot.turn_right()
            bot.turn_right()
        elif reldir == RelativeDirection.Left:
            bot.turn_left()

        board[bot.pos].data.pop('bgcolor', None)

