"""Original PHANS vacancy assignment expressed with scalar arithmetic."""

from research._shared.phans import ExperimentalPHANS


class EngineeringPHANS(ExperimentalPHANS):
    """Keep candidate order, original penalties, and all blockers."""

    def _choose_null_position(self, blocker, candidates, penalties):
        # min retains the first candidate on ties, as original np.argmin does.
        return min(
            candidates,
            key=lambda cell: (
                abs(cell[0] - blocker[0])
                + abs(cell[1] - blocker[1])
                + penalties.get(cell, 0)
            ),
        )

    def _select_null_agents(self, blockers, target_positions):
        """Preserve eligibility and unique sequential choices without NumPy."""
        self._update_null_ag_pos_lst()
        available = list(set(self.null_ag_pos_lst))
        selected = []
        for blocker in blockers:
            remaining = min(
                (
                    len(path) - path.index(blocker) - 1
                    for path in self.tgt_ag_path_lst
                    if blocker in path
                ),
                default=float("inf"),
            )
            excluded = set()
            penalties = {}
            for i, path in enumerate(self.tgt_ag_path_lst):
                current = self.tgt_cur_steps[i]
                if blocker in path:
                    index = path.index(blocker)
                    tx, ty = path[current]
                    for cell in path[index:]:
                        penalties[cell] = max(
                            penalties.get(cell, 0),
                            abs(cell[0] - tx) + abs(cell[1] - ty),
                        )
                for cell in path[current:]:
                    if remaining < len(path) - path.index(cell) - 1:
                        excluded.add(cell)
            candidates = [cell for cell in available if cell not in excluded]
            if not candidates:
                break
            choice = self._choose_null_position(blocker, candidates, penalties)
            selected.append(choice)
            available.remove(choice)
        return selected
