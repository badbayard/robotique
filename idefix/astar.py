import heapq
from typing import Dict, Tuple, List, Optional

from idefix import Board, Position


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def heuristic(a: Position, b: Position):
    return abs(a.x - b.x) + abs(a.y - b.y)


def search(board: Board, start: Position, goal: Position) \
        -> Tuple[Dict[Position, Position], Dict[Position, float]]:
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {
        start: None
    }
    cost_so_far = {
        start: 0
    }

    while not frontier.empty():
        current = frontier.get()  # type: Position

        if current == goal:
            break

        for next_cell in board[current].accessible_neighbours:
            next = next_cell.pos
            new_cost = cost_so_far[current] + 1  # pas de poids
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def reconstruct_path(came_from: Dict[Position, Position],
                     start: Position, goal: Position):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def path(board: Board, start: Position, goal: Position) \
        -> Optional[List[Position]]:
    try:
        return reconstruct_path(search(board, start, goal)[0], start, goal)
    except KeyError:
        return None
