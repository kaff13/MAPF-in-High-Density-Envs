"""Original PHANS A* with indexed reservations and cached hole distances.

Successor order, priorities, state identity, and iteration budget stay original.
Reservation inputs are fixed for the duration of a search, as in PHANS.
"""

import heapq
from itertools import count

import numpy as np

from solver.a_star import AStarFollowingConflict


class IndexedAStar(AStarFollowingConflict):
    """Original A* decisions with indexed constraints and cached hole distance."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._reservations = set(self.moving_obstacles)
        self._edge_reservations = set(self.moving_obstacle_edges)
        self._permanent_from = {}
        for x, y, time in self.moving_obstacles:
            if time < 0:
                cell = (x, y)
                self._permanent_from[cell] = min(
                    self._permanent_from.get(cell, float("inf")), -time
                )
        self._null_xy = np.asarray(self.null_agent_pos_lst)
        self._null_distances = {}

    def _state_valid(self, state):
        x, y = state.location.x, state.location.y
        cell = (x, y)
        return (
            0 <= x < self.dimension[0]
            and 0 <= y < self.dimension[1]
            and cell not in self.obstacles
            and state.time < self._permanent_from.get(cell, float("inf"))
        )

    def _transition_valid(self, state_cur, state_next):
        # Keep the original cycle routine and list ordering, including duplicate
        # edge semantics. Actual PHANS searches disable cycles or have no edges.
        if self.considering_cycle_conflict and self.moving_obstacle_edges:
            return super()._transition_valid(state_cur, state_next)
        x, y, time = state_next.location.x, state_next.location.y, state_next.time
        return (
            (x, y, time) not in self._reservations
            and (x, y, time - 1) not in self._reservations
            and (x, y, time + 1) not in self._reservations
            and (x, y, state_cur.location.x, state_cur.location.y) not in self._edge_reservations
        )

    def _null_distance(self, x, y):
        cell = (x, y)
        if cell not in self._null_distances:
            self._null_distances[cell] = (
                np.abs(self._null_xy - np.asarray(cell)).sum(axis=1).min()
            )
        return self._null_distances[cell]

    def _search(self):
        # Same ordering and state identity as solver/a_star.py. The only change
        # inside the loop is memoization of its time-independent hole distance.
        initial_state = self.agent["start"]
        closed_set = set()
        open_set = {initial_state}
        came_from = {}
        g_score = {initial_state: 0}
        h_score = self._admissible_heuristic(initial_state)
        f_score = {initial_state: h_score}
        heap = []
        index = count(0)
        heapq.heappush(heap, (f_score[initial_state], h_score, next(index), initial_state))

        while open_set and (self.a_star_max_iter == -1 or self.iter < self.a_star_max_iter):
            self.iter += 1
            current = heapq.heappop(heap)[3]
            if self._is_at_goal(current):
                return self._reconstruct_path(came_from, current)
            open_set -= {current}
            closed_set |= {current}
            for neighbor in self._get_neighbors(current):
                if neighbor in closed_set:
                    continue
                tentative_g_score = g_score.setdefault(current, float("inf")) + 1
                dst_add = 0
                if self.is_dst_add:
                    dst_to_null = self._null_distance(neighbor.location.x, neighbor.location.y)
                    if dst_to_null > 0 and dst_to_null > tentative_g_score:
                        dst_add = dst_to_null - tentative_g_score
                if neighbor not in open_set:
                    open_set |= {neighbor}
                elif tentative_g_score >= g_score.setdefault(neighbor, float("inf")):
                    continue
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                h_score = self._admissible_heuristic(neighbor)
                f_score[neighbor] = g_score[neighbor] + h_score + dst_add
                heapq.heappush(
                    heap, (f_score[neighbor], h_score, next(index), neighbor)
                )
        return False
