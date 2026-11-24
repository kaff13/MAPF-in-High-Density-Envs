"""PHANS with a fixed execution deadline after the first target advance."""

from research._shared.runtime import solve_planner
from research._shared.phans import ExperimentalPHANS


class CommittedPHANS(ExperimentalPHANS):
    """Reuse phase remainders for at most horizon - 1 extra ticks."""

    def __init__(self, *args, horizon=2, **kwargs):
        if type(horizon) is not int or horizon < 1:
            raise ValueError("horizon must be a positive integer")
        super().__init__(*args, **kwargs)
        self.horizon = horizon
        self._commit_end = None

    def _continue_phase(self, target_moved, phase_ticks, null_paths):
        """Decide after a tick; later advances never extend the deadline."""
        if self.horizon == 1:
            return not target_moved
        if phase_ticks == 1:
            self._commit_end = None
        if target_moved and self._commit_end is None:
            self._commit_end = phase_ticks + self.horizon - 1
        if self._commit_end is None:
            return True

        # Original PHANS refreshes these only between phases. A continuing
        # executor must refresh them now, including targets that just finished.
        for i, path in enumerate(self.tgt_ag_path_lst):
            self.tgt_cur_steps[i] = (
                len(path) - path[::-1].index(self.ag_cur_pos_lst[i]) - 1
            )
        self._update_goal_ag()
        if phase_ticks >= self._commit_end or len(self.goal_ag_idx_lst) == self.task_len:
            return False

        # Old null paths assumed previous target positions. Drop a conflicting
        # remainder instead of allowing it to swap an advanced target.
        targets = set(self.ag_cur_pos_lst[:self.task_len])
        for path in null_paths:
            if targets.intersection(path):
                path.clear()
        if any(len(path) > 1 for path in null_paths):
            return True
        occupied = set(self.ag_cur_pos_lst)
        return any(
            self.tgt_cur_steps[i] + 1 < len(path)
            and path[self.tgt_cur_steps[i] + 1] not in occupied
            for i, path in enumerate(self.tgt_ag_path_lst)
        )


def solve_with_horizon(instance, horizon):
    """Run raw PHANS with a positive, explicitly selected execution horizon."""
    return solve_planner(
        instance,
        planner_class=CommittedPHANS,
        planner_kwargs={"horizon": horizon},
    )


def h2(instance):
    """Allow at most one extra tick after the first target advance."""
    return solve_with_horizon(instance, 2)


def h4(instance):
    """Allow at most three extra ticks after the first target advance."""
    return solve_with_horizon(instance, 4)


def solve(instance):
    """Canonical entrypoint: horizon two and no blocker cutoff."""
    return h2(instance)
