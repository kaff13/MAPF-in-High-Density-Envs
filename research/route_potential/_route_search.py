"""Clearance route scores on the original PHANS object-state A*.

Only target-route scoring changes. Neighbor generation, transition validation,
null-route searches, and NumPy vacancy-distance arithmetic remain original.
These experimental scores are not admissible time lower bounds.
"""

from heapq import heappop, heappush
from itertools import count

import numpy as np

from solver.a_star import AStarFollowingConflict


class ClearanceAStar(AStarFollowingConflict):
    """Keep original transitions; score target routes by clearance cost."""

    default_blocker_cost = 3
    default_hole_weight = 0
    use_potential = False
    accumulate_penalty = True

    def __init__(self, *args, blocker_cost=None, hole_weight=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocker_cost = (
            self.default_blocker_cost if blocker_cost is None else blocker_cost
        )
        self.hole_weight = (
            self.default_hole_weight if hole_weight is None else hole_weight
        )
        self._occupied = set(self.agent_start_pos_lst)
        self._goal_potential = (
            self._build_goal_potential()
            if self.use_potential and self.is_dst_add
            else {}
        )

    def _null_distance(self, x, y):
        # Keep the original per-neighbor NumPy calculation, without a cache.
        neighbor_xy = np.array((x, y))
        null_xy = np.array(self.null_agent_pos_lst)
        return np.abs(null_xy - neighbor_xy).sum(axis=1).min()

    def _build_goal_potential(self):
        """Relax backwards using the cost of forward entry into a cell."""
        goal = self.agent["goal"].location
        origin = (goal.x, goal.y)
        best = {origin: 0}
        heap = [(0, origin)]
        width, height = self.dimension
        while heap:
            cost, (x, y) = heappop(heap)
            if cost != best[(x, y)]:
                continue
            # Reverse relaxation charges forward entry into the popped cell.
            enter_cost = 1 + (
                self.blocker_cost
                + self.hole_weight * min(5, self._null_distance(x, y))
                if (x, y) in self._occupied
                else 0
            )
            for nx, ny in ((x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)):
                cell = (nx, ny)
                if not (0 <= nx < width and 0 <= ny < height) or cell in self.obstacles:
                    continue
                new_cost = cost + enter_cost
                if new_cost < best.get(cell, float("inf")):
                    best[cell] = new_cost
                    heappush(heap, (new_cost, cell))
        return best

    def _search(self):
        """Keep weighted g separate from the physical time in each state."""
        if (
            not self.is_dst_add
            or (self.blocker_cost == 0 and self.hole_weight == 0)
            or (self.considering_cycle_conflict and self.moving_obstacle_edges)
        ):
            return super()._search()

        initial = self.agent["start"]
        initial_cell = (initial.location.x, initial.location.y)
        infinity = float("inf")
        initial_h = (
            self._goal_potential.get(initial_cell, infinity)
            if self.use_potential else self._admissible_heuristic(initial)
        )
        serial = count()
        heap = [(initial_h, initial_h, next(serial), 0, initial)]
        best = {initial: 0}
        parents = {}
        closed = set()

        while heap and (self.a_star_max_iter == -1 or self.iter < self.a_star_max_iter):
            _, _, _, cost, current = heappop(heap)
            if cost != best[current] or current in closed:
                continue
            self.iter += 1
            if self._is_at_goal(current):
                return self._reconstruct_path(parents, current)
            closed.add(current)

            # The original implementation owns all movement/conflict checks.
            for neighbor in self._get_neighbors(current):
                if neighbor in closed:
                    continue
                nx, ny = neighbor.location.x, neighbor.location.y
                cell = (nx, ny)
                moved = neighbor.location != current.location
                penalty = 0
                if cell in self._occupied and moved:
                    penalty = self.blocker_cost + self.hole_weight * min(
                        5, self._null_distance(nx, ny)
                    )
                new_cost = cost + 1 + (penalty if self.accumulate_penalty else 0)
                if new_cost >= best.get(neighbor, infinity):
                    continue
                best[neighbor] = new_cost
                parents[neighbor] = current
                heuristic = (
                    self._goal_potential.get(cell, infinity)
                    if self.use_potential else self._admissible_heuristic(neighbor)
                )

                # Preserve the prior weighted idea's local null-arrival bias.
                dst_add = 0
                null_distance = self._null_distance(nx, ny)
                if 0 < null_distance > neighbor.time:
                    dst_add = null_distance - neighbor.time
                heappush(
                    heap,
                    (new_cost + heuristic + dst_add, heuristic,
                     next(serial), new_cost, neighbor),
                )
        return False


class Block2AStar(ClearanceAStar):
    default_blocker_cost = 2


class Block4AStar(ClearanceAStar):
    default_blocker_cost = 4


class Block2HoleAStar(ClearanceAStar):
    default_blocker_cost = 2
    default_hole_weight = 1


class Potential2AStar(Block2AStar):
    """Penalty two is accumulated in g and used by the reverse potential."""

    use_potential = True


class Potential1AStar(Potential2AStar):
    default_blocker_cost = 1


class Potential3AStar(Potential2AStar):
    default_blocker_cost = 3


class PotentialOnly2AStar(Potential2AStar):
    """Unit-cost g with a weighted potential used only for ordering."""

    accumulate_penalty = False


class Potential2HoleQuarterAStar(Potential2AStar):
    default_hole_weight = 0.25


class Potential2HoleHalfAStar(Potential2AStar):
    default_hole_weight = 0.5
