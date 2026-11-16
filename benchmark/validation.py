"""Independent validator for synchronous MAPF-HD traces."""

from dataclasses import dataclass

from .maps import Instance, point


@dataclass(frozen=True)
class TraceCheck:
    status: str
    makespan: int | None = None
    detail: str = ""


def check_trace(instance: Instance, frames) -> TraceCheck:
    if frames is None:
        return TraceCheck("unsolved", detail="no trace returned")
    try:
        frames = iter(frames)
    except TypeError:
        return TraceCheck("invalid", detail="trace is not iterable")

    previous = None
    makespan = None
    goals = instance.map.goals
    for tick, raw_frame in enumerate(frames):
        try:
            frame = tuple(point(cell) for cell in raw_frame)
        except (TypeError, ValueError, OverflowError):
            return TraceCheck("invalid", detail=f"tick {tick}: expected integer cell pairs")
        if len(frame) != len(instance.starts):
            return TraceCheck("invalid", detail=f"tick {tick}: wrong agent count")
        occupied = set()
        previous_occupied = set(previous or ())
        for agent, cell in enumerate(frame):
            if not instance.map.is_free(cell):
                return TraceCheck("invalid", detail=f"tick {tick}: agent {agent} outside traversable grid")
            if cell in occupied:
                return TraceCheck("invalid", detail=f"tick {tick}: vertex conflict at {cell}")
            occupied.add(cell)
            if previous is None or cell == previous[agent]:
                continue
            x, y = previous[agent]
            if abs(x - cell[0]) + abs(y - cell[1]) != 1:
                return TraceCheck("invalid", detail=f"tick {tick}: non-adjacent move by agent {agent}")
            if cell in previous_occupied:
                return TraceCheck("invalid", detail=f"tick {tick}: following conflict by agent {agent} at {cell}")
        if previous is None and frame != instance.starts:
            return TraceCheck("invalid", detail="tick 0: starts or agent order differ")
        if makespan is None and frame[:len(goals)] == goals:
            makespan = tick
        previous = frame
    if makespan is None:
        return TraceCheck("unsolved", detail="trace ended before all goals were reached")
    return TraceCheck("solved", makespan)
