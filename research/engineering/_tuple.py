"""Exact PHANS A* ablation using integer tuple states internally."""

import heapq
from itertools import count

from solver.a_star import Location, State

from ._indexed import IndexedAStar


class TupleAStar(IndexedAStar):
    """Preserve PHANS' heap order while avoiding string hashes and state objects.

    Every transition costs one and increments time by one. Therefore every path
    to (t,x,y) has g=t, so an already open state never needs a decrease-key.
    States are converted back to the baseline representation only for output.
    """

    def _search(self):
        if self.considering_cycle_conflict and self.moving_obstacle_edges:
            # This uncommon API mode needs the original list-based cycle logic.
            return super()._search()

        start = self.agent["start"].location
        goal = self.agent["goal"].location
        initial = (0, start.x, start.y)
        gx, gy = goal.x, goal.y
        width, height = self.dimension
        obstacles = self.obstacles
        reservations = self._reservations
        edge_reservations = self._edge_reservations
        permanent_from = self._permanent_from
        infinity = float("inf")
        initial_h = float(abs(start.x - gx) + abs(start.y - gy))
        index = count()
        heap = [(initial_h, initial_h, next(index), initial)]
        open_set = {initial}
        closed_set = set()
        parents = {}

        while open_set and (self.a_star_max_iter == -1 or self.iter < self.a_star_max_iter):
            self.iter += 1
            current = heapq.heappop(heap)[3]
            time, x, y = current
            if (x, y) == (gx, gy):
                path = [current]
                while current in parents:
                    current = parents[current]
                    path.append(current)
                return [State(t, Location(px, py)) for t, px, py in reversed(path)]
            open_set.remove(current)
            closed_set.add(current)
            next_time = time + 1
            # The order is part of exact tie-breaking: wait, up, down, left, right.
            for nx, ny in ((x, y), (x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)):
                cell = (nx, ny)
                if not (
                    0 <= nx < width
                    and 0 <= ny < height
                    and cell not in obstacles
                    and next_time < permanent_from.get(cell, infinity)
                    and (nx, ny, next_time) not in reservations
                    and (nx, ny, next_time - 1) not in reservations
                    and (nx, ny, next_time + 1) not in reservations
                    and (nx, ny, x, y) not in edge_reservations
                ):
                    continue
                neighbor = (next_time, nx, ny)
                if neighbor in closed_set:
                    continue
                dst_add = 0
                if self.is_dst_add:
                    dst_to_null = self._null_distance(nx, ny)
                    if dst_to_null > 0 and dst_to_null > next_time:
                        dst_add = dst_to_null - next_time
                if neighbor in open_set:
                    continue
                open_set.add(neighbor)
                parents[neighbor] = current
                heuristic = float(abs(nx - gx) + abs(ny - gy))
                heapq.heappush(
                    heap,
                    (next_time + heuristic + dst_add, heuristic, next(index), neighbor),
                )
        return False
