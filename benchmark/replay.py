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
    payload = {
        "instance": instance.to_json(),
        "frames": normalized,
        "solver": solver_name,
        "status": checked.status,
        "reported_status": status,
        "detail": detail or checked.detail,
        "makespan": checked.makespan,
    }
    # JSON is inside a raw-text script element: HTML escaping alone is unsafe.
    embedded = json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    for character, escaped in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"),
                               ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        embedded = embedded.replace(character, escaped)
    template = Path(__file__).with_name("replay.html").read_text(encoding="utf-8")
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
