from io import StringIO
from typing import List, Iterator, Optional, Tuple

from flask import render_template, Markup, jsonify, request

from idefix import Board, FakeBot, Bot, Wall, Direction, Position, boardgen, \
    RelativeDirection, discovery
from idefix.proxy import ProxyBot
from idefix.webui import app

import idefix.ricochet.model as rm
import idefix.ricochet.ricochet as rr


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

    def __init__(self, board: Board, bots: List[Bot],
                 destination: Optional[Position] = None,
                 destbot: Optional[Bot] = None):
        self.board = board
        self.bots = bots
        self.destination = destination
        self.destbot = destbot

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
                if None not in (self.destination, self.destbot):
                    if x == self.destination.x and y == self.destination.y:
                        content = '★'
                        bgcolor = [*self.destbot.color, 1]
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
                out.write('" data-x="{}" data-y="{}">'.format(x, y))
                out.write(content)
                out.write('</td>')
            out.write('</tr>')
        out.write('</table>')
        return out.getvalue()


class Context:
    def __init__(self):
        self.realboard = None  # type: Board
        self.board = None  # type: Board
        self.red = None  # type: ProxyBot
        self.green = None  # type: ProxyBot
        self.blue = None  # type: ProxyBot
        self.bots = None  # type: List[ProxyBot]
        self.disc = None  # type: Iterator
        self.raw_instructions = []  # type: List[Tuple[Bot, Direction]]
        self.instructions = []  # type: List
        self.destination = None  # type: Optional[Position]
        self.destbot = None  # type: Optional[Bot]

    def make_board_discovery(self):
        self.realboard = boardgen.generate_board(8, 8)
        self.board = Board(8, 8)
        fakebot = FakeBot(self.realboard)
        fakebot.dir = Direction.East
        fakebot.write_info(self.board)
        self.red = ProxyBot(fakebot)
        self.bots = [self.red]
        self.disc = discovery.run(self.board, self.red)

    def _find_empty_cell(self):
        for y in range(self.board.min_y, self.board.max_y + 1):
            for x in range(self.board.min_x, self.board.max_x + 1):
                pos = Position(x, y)
                cell = self.board[pos]
                if cell.explored or any([bot.pos == pos for bot in self.bots]):
                    continue
                return cell

    def prepare_game(self):
        self.green = ProxyBot(FakeBot(
            self.board, name='green', color=[0, 255, 0]))
        self.blue = ProxyBot(FakeBot(
            self.board, name='blue', color=[0, 0, 255]))
        self.bots = [self.red, self.green, self.blue]
        self.green.pos = self._find_empty_cell().pos
        self.blue.pos = self._find_empty_cell().pos

    def translate_instructions(self):
        pass  # TODO


ctx = Context()
ctx.make_board_discovery()


def _render(commands: Optional[List] = None,
            discovery_end: Optional[bool] = None):
    view = HTMLTableBoardView(ctx.board, ctx.bots, ctx.destination, ctx.destbot)
    viewreal = HTMLTableBoardView(ctx.realboard, ctx.bots, ctx.destination, ctx.destbot)
    json = {
        'board': view.render(),
        'realboard': viewreal.render()
    }
    if commands is not None:
        json['commands'] = commands
    if discovery_end is not None:
        json['discovery_end'] = discovery_end
    return jsonify(json)


@app.route('/')
def index():
    view = HTMLTableBoardView(ctx.board, ctx.bots, ctx.destination, ctx.destbot)
    return render_template("index.html", board1=Markup(view.render()))


@app.route('/step_discovery')
def step_discovery():
    try:
        commands = next(ctx.disc)
    except StopIteration:
        commands = None
    return _render(commands=commands, discovery_end=commands is None)


@app.route('/auto_discovery')
def auto_discovery():
    commands = []
    try:
        while True:
            commands.extend(next(ctx.disc))
    except StopIteration:
        pass
    return _render(commands=commands)


@app.route('/reset')
def reset():
    global ctx
    ctx = Context()
    ctx.make_board_discovery()
    return _render()


@app.route('/prepare_game')
def prepare_game():
    ctx.prepare_game()
    return _render()


@app.route('/start_game')
def start_game():
    rgame = rm.Game(ctx.board, ctx.bots, ctx.destination, ctx.destbot)
    ctx.raw_instructions = rr.search(rgame)
    commands = []
    for i in ctx.raw_instructions:
        commands.append({'bot': i[0].name, 'cmd': str(i[1])})
    return _render(commands=commands)


@app.route('/place_bot')
def place_bot():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    botname = request.args.get('bot')
    bot = [b for b in ctx.bots if b.name == botname][0]
    newpos = Position(x, y)
    if bot.dir == Direction.Unknown:
        bot.dir = Direction.North
    if bot.pos == newpos:
        bot.dir = bot.dir.apply_relative(RelativeDirection.Right)
    else:
        bot.pos = newpos
    return _render()


@app.route('/place_dest')
def place_dest():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    botname = request.args.get('bot')
    ctx.destbot = [b for b in ctx.bots if b.name == botname][0]
    ctx.destination = Position(x, y)
    return _render()
