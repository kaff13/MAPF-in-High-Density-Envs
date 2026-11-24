"""Correct a vacancy choice only when static obstacles force a detour."""

from collections import deque

from research._shared.phans import ExperimentalPHANS


def has_manhattan_path(start, goal, blocked):
    """Search only steps that strictly reduce distance to the chosen vacancy."""
    frontier = [start]
    seen = {start}
    while frontier:
        x, y = frontier.pop()
        if (x, y) == goal:
            return True
        choices = []
        if x != goal[0]:
            choices.append((x + (1 if goal[0] > x else -1), y))
        if y != goal[1]:
            choices.append((x, y + (1 if goal[1] > y else -1)))
        for cell in choices:
            if cell not in blocked and cell not in seen:
                seen.add(cell)
                frontier.append(cell)
    return False


def nearest_holes(start, holes, dimension, blocked, limit):
    """BFS until limit eligible holes are reached, returning their distances."""
    width, height = dimension
    queue = deque([start])
    distance = {start: 0}
    found = {}
    while queue and len(found) < limit:
        x, y = queue.popleft()
        if (x, y) in holes:
            found[(x, y)] = distance[(x, y)]
            if len(found) == limit:
                break
        for cell in ((x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)):
            nx, ny = cell
            if (
                0 <= nx < width
                and 0 <= ny < height
                and cell not in blocked
                and cell not in distance
            ):
                distance[cell] = distance[(x, y)] + 1
                queue.append(cell)
    return found


class DetourPHANS(ExperimentalPHANS):
    """Retain the original choice whenever a Manhattan-length path exists."""

    def __init__(
        self, size_x, size_y, static_obstacles=None, *,
        detour_enabled=True, lookahead=None,
    ):
        super().__init__(
            size_x, size_y, static_obstacles=static_obstacles, lookahead=lookahead
        )
        self.detour_enabled = detour_enabled
        self._phase_blockers = set()

    def _select_null_agents(self, blockers, target_positions):
        """Expose phase blockers only while inherited assignment runs."""
        previous = self._phase_blockers
        self._phase_blockers = set(blockers)
        try:
            return super()._select_null_agents(blockers, target_positions)
        finally:
            self._phase_blockers = previous

    def _choose_null_position(self, blocker, candidates, penalties):
        original = super()._choose_null_position(blocker, candidates, penalties)
        if not self.detour_enabled:
            return original

        blocked = set(self.static_obss) | (
            set(self.ag_cur_pos_lst[:self.task_len]) - self._phase_blockers
        )
        for i, path in enumerate(self.tgt_ag_path_lst):
            if blocker in path:
                blocked.update(path[self.tgt_cur_steps[i]:path.index(blocker)])
        if has_manhattan_path(blocker, original, blocked):
            return original

        dimension = (self.size_x, self.size_y)
        distances = nearest_holes(blocker, set(candidates), dimension, blocked, 8)
        # Keep the original hole even when it lies beyond the first eight.
        distances.update(nearest_holes(blocker, {original}, dimension, blocked, 1))
        if not distances:
            return original
        return min(
            distances,
            key=lambda cell: (distances[cell] + penalties.get(cell, 0), cell),
        )
