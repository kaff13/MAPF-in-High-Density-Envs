"""Isolated solver execution with a shared wall-clock budget."""

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, replace
from hashlib import sha256
import gzip
from importlib import import_module
from inspect import getsourcefile
from multiprocessing import get_context
from pathlib import Path
from time import perf_counter
import os
import json
import random
import subprocess
import sys
import traceback

from .maps import IDENTIFIER, Instance, point
from .validation import check_trace

ROOT = Path(__file__).resolve().parents[1]
PHANS_COMMIT = "a82ed819d37932ff845e170805f41e24c82e550b"
PHANS_PARAMETERS = {"a_star_max_iter": -1, "max_loop": 300}
SETUP_TIMEOUT_S = 60
VALIDATION_TIMEOUT_S = 120


@dataclass(frozen=True)
class Solver:
    name: str
    entrypoint: str | None = None

    @classmethod
    def parse(cls, spec):
        if spec == "phans":
            return cls("phans")
        name, equals, entrypoint = spec.partition("=")
        module, colon, function = entrypoint.partition(":")
        if (
            not equals or not colon or not IDENTIFIER.fullmatch(name) or name.casefold() == "phans"
            or not all(part.isidentifier() for part in module.split("."))
            or not function.isidentifier()
        ):
            raise ValueError("use 'phans' or NAME=python.module:function for --solver")
        return cls(name, entrypoint)


@dataclass(frozen=True)
class Attempt:
    status: str
    computation_time_s: float | None = None
    makespan: int | None = None
    detail: str = ""
    source_sha256: str | None = None
    plan_path: str | None = None


def extract_baseline(destination: Path):
    """Write the pinned source into a private, transient import root."""
    (destination / "solver").mkdir(parents=True)
    (destination / "solver" / "__init__.py").touch()
    for relative in ("solver/phans_null_agent_swapping.py", "solver/a_star.py", "LICENCE.md"):
        result = subprocess.run(
            ["git", "show", f"{PHANS_COMMIT}:{relative}"],
            cwd=ROOT, capture_output=True, check=False,
        )
        if result.returncode:
            raise ValueError(f"Missing PHANS commit {PHANS_COMMIT}. Fetch full history from upstream.")
        (destination / relative).write_bytes(result.stdout)


def load_solver(solver: Solver, baseline_root: Path):
    if solver.entrypoint is None:
        sys.path.insert(0, str(baseline_root))
        phans = import_module("solver.phans_null_agent_swapping").PHANS

        def solve(instance: Instance):
            grid = instance.map
            planner = phans(grid.width, grid.height, static_obstacles=sorted(grid.walls))
            return planner.run_loop(list(instance.starts), list(grid.goals), **PHANS_PARAMETERS)

        return solve
    module, function = solver.entrypoint.split(":")
    entrypoint = getattr(import_module(module), function)
    if not callable(entrypoint):
        raise TypeError("solver entrypoint is not callable")
    return entrypoint


def fingerprint_source(solve):
    try:
        source = getsourcefile(solve)
        return sha256(Path(source).read_bytes()).hexdigest() if source else None
    except (TypeError, OSError):
        return None


def materialize_frame(frame):
    if type(frame) in (list, tuple):
        return frame
    try:
        cells = iter(frame)
    except TypeError:
        return frame
    return tuple(cells)


def materialize_trace(frames):
    try:
        sequence = iter(frames)
    except TypeError:
        return frames
    return [materialize_frame(frame) for frame in sequence]


def save_plan(path, instance, solver, check, frames):
    if path is None or frames is None or check.status == "invalid":
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized_frames = [[point(cell) for cell in frame] for frame in frames]
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        with gzip.open(temporary, "wt", encoding="utf-8") as stream:
            json.dump({
                "instance_id": instance.id, "solver": solver.name,
                "status": check.status, "makespan": check.makespan,
                "detail": check.detail, "frames": serialized_frames,
            }, stream, separators=(",", ":"))
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return str(path)


def worker(connection, solver, instance, baseline_root, log_path, plan_path=None, source_root=None):
    os.environ.setdefault("MPLBACKEND", "Agg")
    with connection, log_path.open("w", encoding="utf-8", buffering=256 * 1024) as stream:
        with redirect_stdout(stream), redirect_stderr(stream):
            started = None
            elapsed = None
            try:
                if source_root is not None:
                    sys.path.insert(0, str(source_root))
                solve = load_solver(solver, baseline_root)
                fingerprint = fingerprint_source(solve) if solver.entrypoint is not None else None
                random.seed(instance.seed)
                connection.send(("ready", fingerprint))
                connection.recv()
                started = perf_counter()
                frames = materialize_trace(solve(instance))
                elapsed = perf_counter() - started
                connection.send(("finished", elapsed))
                check = check_trace(instance, frames)
                saved = save_plan(plan_path, instance, solver, check, frames)
                stream.flush()
                connection.send(("result", Attempt(check.status, elapsed, check.makespan, check.detail, plan_path=saved)))
            except Exception as error:
                if started is not None and elapsed is None:
                    elapsed = perf_counter() - started
                traceback.print_exc()
                stream.flush()
                connection.send(("result", Attempt("crash", elapsed, detail=f"{type(error).__name__}: {error}")))


def run_attempt(solver, instance, timeout_s, baseline_root, log_path, plan_path=None, source_root=None):
    context = get_context("spawn")
    parent, child = context.Pipe()
    process = context.Process(target=worker, args=(child, solver, instance, baseline_root, log_path, plan_path, source_root))
    with parent, child:
        process.start()
        child.close()
        try:
            if not parent.poll(SETUP_TIMEOUT_S):
                return Attempt("crash", detail="solver setup timed out")
            stage, result = parent.recv()
            if stage == "result":
                return result
            fingerprint = result
            parent.send("start")
            timeout = Attempt("timeout", timeout_s, detail="planning time limit reached", source_sha256=fingerprint)
            if not parent.poll(timeout_s):
                return timeout
            stage, result = parent.recv()
            if stage == "result":
                if result.computation_time_s is not None and result.computation_time_s > timeout_s:
                    return timeout
                return replace(result, source_sha256=fingerprint)
            if result > timeout_s:
                return timeout
            if not parent.poll(VALIDATION_TIMEOUT_S):
                return Attempt("crash", result, detail="trace validation timed out", source_sha256=fingerprint)
            _, attempt = parent.recv()
            return replace(attempt, source_sha256=fingerprint)
        except (EOFError, BrokenPipeError, OSError):
            return Attempt("crash", detail="solver process exited without a result")
        finally:
            process.join(0.05)
            if process.is_alive():
                process.kill()
                process.join()
            process.close()
