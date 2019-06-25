from io import StringIO
from typing import List, Iterator

from flask import render_template, Markup, jsonify

from idefix import Board, FakeBot, Bot, Wall, Direction, Position, boardgen, \
    astar
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
                        bgcolor = [*cell.explored_by.color, 0.5]
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

    @staticmethod
    def clear():
        print('\x1Bc', end='', flush=True)


# TODO: virer tout ça
board = None  # type: Board
discoveryboard = None  # type: Board
bot = None  # type: ProxyBot
discovery = None  # type: Iterator

def run_discovery():
    # On tourne pour savoir l'état des 4 murs autour du robot
    commands = []
    bot.write_info(discoveryboard)
    bot.turn_left()
    bot.write_info(discoveryboard)
    yield bot.command_list
    bot.clear_command_list()
    to_discover = discoveryboard[bot.pos].accessible_neighbours  # type: List[Board.Cell]
    while len(to_discover) != 0:
        '''least_shitty = None
least_shitty_score = float('-inf')
for d in to_discover:
    path = astar.path(discoveryboard, bot.pos, d.pos)
    if path is not None:
        for step in path:
            board[step].data['bgcolor'] = [255, 255, 192]
    least'''
        try:
            fwdcell = discoveryboard[bot.pos.move(bot.dir)]
        except IndexError:
            fwdcell = None
        cell = discoveryboard[bot.pos]
        if cell.wall(bot.dir) == Wall.Yes:
            lwall = cell.wall(bot.dir_left) == Wall.Yes
            rwall = cell.wall(bot.dir_right) == Wall.Yes
            if lwall:
                bot.turn_right()
            elif rwall:
                bot.turn_left()
            elif lwall and rwall:
                bot.turn_left()
                bot.turn_left()
            else:
                bot.turn_left()
        else:
            if fwdcell is not None and fwdcell.explored:
                lwall = cell.wall(bot.dir_left) == Wall.Yes
                rwall = cell.wall(bot.dir_right) == Wall.Yes
                if not lwall:
                    bot.turn_left()
                elif not rwall:
                    bot.turn_right()
                else:
                    pass
            else:
                bot.forward()
        bot.write_info(discoveryboard)
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
    from idefix import astar
    #print(astar.search(board, Position(0, 0), Position(4, 4)))
    try:
        path = astar.reconstruct_path(astar.search(board, Position(0, 0), Position(4, 4))[0], Position(0, 0), Position(4, 4))
        for step in path:
            board[step].data['bgcolor'] = [255, 255, 192]
    except KeyError:
        pass
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
