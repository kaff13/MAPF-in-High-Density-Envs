"""Export independently validated traces as portable, offline HTML players."""

import gzip
import json
from pathlib import Path
import tempfile

from .maps import Instance, point
from .validation import check_trace


def load_plan(path: Path) -> dict:
    """Read a saved plan object from UTF-8 JSON or ``.gz`` compressed JSON."""
    path = Path(path)
    opener = gzip.open if path.suffix.lower() == ".gz" else open
    try:
        with opener(path, "rt", encoding="utf-8") as stream:
            plan = json.load(stream)
    except (OSError, UnicodeError, ValueError, EOFError) as error:
        raise ValueError(f"cannot read plan {path}: {error}") from error
    if not isinstance(plan, dict):
        raise ValueError(f"plan {path}: expected a JSON object")
    return plan


def write_replay(
    instance: Instance,
    frames,
    output: Path,
    *,
    solver_name: str = "",
    status: str = "",
    detail: str = "",
) -> Path:
    """Write a self-contained player, preserving all supplied frames and waits.

    ``status`` records the solver's reported outcome. The visible trace outcome
    is always independently checked; an incomplete trace cannot claim solved.
    Invalid traces raise ``ValueError`` before an existing output is changed.
    ``makespan`` is the first solved tick, even if later frames are supplied.
    """
    payload = {"instance": instance.to_json(), **_trace_data(
        instance, frames, solver_name=solver_name, status=status, detail=detail,
    )}
    return _write_html(payload, output, "replay.html")


def write_paired_replay(
    instance: Instance, baseline_plan: dict, candidate_plan: dict, output: Path,
    *, baseline_name="PHANS", candidate_name=None,
) -> Path:
    """Compare two traces of one scenario, with baseline left and candidate right.

    The shared timeline ends at the longer trace's last tick. The player holds
    the shorter trace's final frame and starts paused. Each side shows the
    checked trace result separately from the recorded solver result.
    """
    plans = {}
    for side, plan in (("baseline", baseline_plan), ("candidate", candidate_plan)):
        try:
            if not isinstance(plan, dict):
                raise ValueError("expected a plan object")
            if "instance_id" in plan and plan["instance_id"] != instance.id:
                raise ValueError("plan instance_id differs from the selected instance")
            if "instance" in plan and Instance.from_json(plan["instance"]) != instance:
                raise ValueError("plan instance differs from the selected instance")
            plans[side] = _trace_data(
                instance, plan.get("frames"), solver_name=plan.get("solver", ""),
                status=plan.get("status", ""), detail=plan.get("detail", ""),
            )
            plans[side]["trace_available"] = plan.get("trace_available", True)
            if not plans[side]["trace_available"]:
                plans[side]["status"] = "unavailable"
                plans[side]["makespan"] = None
            for key in ("provenance", "recorded_status", "replay_attempt"):
                if key in plan:
                    plans[side][key] = plan[key]
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"{side}: {error}") from error
    payload = {
        "instance": instance.to_json(), **plans,
        "max_tick": max(plan["last_tick"] for plan in plans.values()),
        "baseline_name": baseline_name,
        "candidate_name": candidate_name or plans["candidate"]["solver"],
        "autoplay": False,
    }
    return _write_html(payload, output, "paired_replay.html")


def _trace_data(instance, frames, *, solver_name, status, detail):
    normalized = []
    try:
        iterator = iter(frames)
    except TypeError as error:
        raise ValueError("trace must contain at least one frame") from error
    for tick, frame in enumerate(iterator):
        try:
            normalized.append([list(point(cell)) for cell in frame])
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError(f"tick {tick}: expected integer cell pairs") from error
    if not normalized:
        raise ValueError("trace must contain at least one frame")
    checked = check_trace(instance, normalized)
    if checked.status == "invalid":
        raise ValueError(checked.detail)
    return {
        "frames": normalized,
        "solver": solver_name,
        "status": checked.status,
        "reported_status": status,
        "detail": detail or checked.detail,
        "makespan": checked.makespan,
        "last_tick": len(normalized) - 1,
    }


def _write_html(payload, output, template_name):
    # JSON is inside a raw-text script element: HTML escaping alone is unsafe.
    embedded = json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    for character, escaped in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"),
                               ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        embedded = embedded.replace(character, escaped)
    template = Path(__file__).with_name(template_name).read_text(encoding="utf-8")
    document = template.replace("__REPLAY_DATA__", embedded)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=output.parent, delete=False, suffix=".tmp") as stream:
            temporary = Path(stream.name)
            stream.write(document)
        temporary.replace(output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return output
