from io import StringIO
from typing import List, Iterator

from flask import render_template, Markup, jsonify

from idefix import Board, FakeBot, Bot, Wall, Direction, Position, boardgen, \
    astar, RelativeDirection
from idefix.proxy import ProxyBot
from idefix.webui import app


class HTMLTableBoardView:
    HorizontalWalls = {
        Wall.Unknown: 'wt-u',
        Wall.Yes: 'wt-y',
        Wall.No: 'wt-n'
    }
    VerticalWalls = {
        Wall.Unknown: 'wl-u',
        Wall.Yes: 'wl-y',
        Wall.No: 'wl-n'
    }

    def __init__(self, board: Board, bots: List[Bot]):
        self.board = board
        self.bots = bots

    def render(self):
        board = self.board
        out = StringIO()
        out.write('<table class="robotgrid">')
        for y in range(board.min_y, board.max_y + 1):
            out.write('<tr>')
            for x in range(board.min_x, board.max_x + 1):
                cell = board[Position(x, y)]
                classes = []
                content = ''
                bgcolor = None
                # styles = []
                if y != board.min_y:
                    classes.append(
                        self.HorizontalWalls[cell.wall(Direction.North)])
                if x != board.min_x:
                    classes.append(
                        self.VerticalWalls[cell.wall(Direction.West)])
                if cell.explored:
                    if cell.explored_by is not None:
                        bgcolor = [*cell.explored_by.color, 0.2]
                else:
                    classes.append('c-unexp')
                    content = '?'
                if 'bgcolor' in cell.data:
                    bgcolor = cell.data['bgcolor']  # type: List[int]
                    if len(bgcolor) == 3:
                        bgcolor.append(1)
                for bot in self.bots:
                    if x == bot.pos.x and y == bot.pos.y:
                        content = {
                            Direction.North: '↑',
                            Direction.East: '→',
                            Direction.South: '↓',
                            Direction.West: '←',
                            Direction.Unknown: '¿'
                        }[bot.dir]
                        bgcolor = [*bot.color, 1]
                out.write('<td class="')
                out.write(' '.join(classes))
                out.write('" style="')
                if bgcolor:
                    out.write('background-color:rgba({},{},{},{})'.format(
                        *bgcolor))
                # out.write(';'.join(styles))
                out.write('">')
                out.write(content)
                out.write('</td>')
            out.write('</tr>')
        out.write('</table>')
        return out.getvalue()


# TODO: virer tout ça
board = None  # type: Board
discoveryboard = None  # type: Board
bot = None  # type: ProxyBot
discovery = None  # type: Iterator


def run_discovery():
    # On tourne pour savoir l'état des 4 murs autour du robot
    def mark_candidates(candidates):
        for cell in candidates:
            if Wall.No in (
                    cell.wall(Direction.North), cell.wall(Direction.East),
                    cell.wall(Direction.South), cell.wall(Direction.West)):
                cell.data['bgcolor'] = [255, 255, 128]

    def get_candidates() -> List[Board.Cell]:
        ret = []
        for y in range(discoveryboard.min_y, discoveryboard.max_y + 1):
            for x in range(discoveryboard.min_x, discoveryboard.max_x + 1):
                cell = discoveryboard[Position(x, y)]
                if cell.explored:
                    continue
                if Wall.No in (
                        cell.wall(Direction.North), cell.wall(Direction.East),
                        cell.wall(Direction.South), cell.wall(Direction.West)):
                    ret.append(cell)
        return ret
    bot.write_info(discoveryboard)
    mark_candidates(get_candidates())
    yield []
    bot.turn_left()
    bot.write_info(discoveryboard)
    mark_candidates(get_candidates())
    yield bot.command_list
    bot.clear_command_list()
    while True:
        candidates = get_candidates()
        if len(candidates) == 0:
            break
        candidates_paths = [*map(
            lambda d: astar.path(discoveryboard, bot.pos, d.pos), candidates)]
        shortest_idx = min(enumerate(candidates_paths),
                           key=lambda x: len(x[1]))[0]

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
        mark_candidates(candidates)
        candidates[shortest_idx].data['bgcolor'] = [255, 255, 0]
        bot.write_info(discoveryboard)
        discoveryboard[bot.pos].data.pop('bgcolor', None)

        yield bot.command_list
        bot.clear_command_list()


def mkboard():
    global board, discoveryboard, bot, discovery
    board = boardgen.generate_board(5, 5)
    discoveryboard = Board(5, 5)
    fakebot = FakeBot(board)
    fakebot.dir = Direction.East
    fakebot.write_info(discoveryboard)
    bot = ProxyBot(fakebot)
    discovery = run_discovery()
mkboard()


@app.route('/')
def index():
    view = HTMLTableBoardView(discoveryboard, [bot])
    viewreal = HTMLTableBoardView(board, [bot])
    return render_template("index.html", board1=Markup(view.render() + viewreal.render()))


@app.route('/step')
def step():
    commands = next(discovery)
    view = HTMLTableBoardView(discoveryboard, [bot])
    viewreal = HTMLTableBoardView(board, [bot])
    return jsonify({
        'board': view.render()+viewreal.render(),
        'commands': commands
    })


@app.route('/reset')
def reset():
    mkboard()
    view = HTMLTableBoardView(discoveryboard, [bot])
    viewreal = HTMLTableBoardView(board, [bot])
    return jsonify({
        'board': view.render()+viewreal.render(),
        'commands': []
    })


@app.route('/about')
def about():
    return render_template("about.html")
