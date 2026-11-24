"""Durable campaign records and a process lock, independent of solver timing."""
from contextlib import AbstractContextManager
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile

from .artifacts import inside_run
from .reports import validate_results


def digest(data):
    return sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    result = sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def atomic_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


class CampaignLock(AbstractContextManager):
    """OS-held lock: interruption releases ownership without stale-PID guessing."""

    def __init__(self, path):
        self.path = Path(path)
        self.stream = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.stream = self.path.open("a+b")
        if self.stream.seek(0, 2) == 0:
            self.stream.write(b"0")
            self.stream.flush()
        self.stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            self.stream.close()
            self.stream = None
            raise RuntimeError("campaign is already locked by another process") from error
        return self

    def __exit__(self, *args):
        if self.stream is not None:
            self.stream.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream.fileno(), fcntl.LOCK_UN)
            self.stream.close()
        return False


def save_checkpoint(root, row, configuration_digest, instance_digest):
    path = root / "checkpoints" / row["solver"] / (row["instance_id"] + ".json")
    if path.exists():
        raise ValueError("checkpoint already exists; refusing to replace measurements")
    plan = inside_run(root, row["plan_path"]) if row["plan_path"] else None
    atomic_json(path, {
        "configuration_digest": configuration_digest,
        "instance_digest": instance_digest,
        "row": row, "row_digest": digest(row),
        "plan_sha256": file_hash(plan) if plan is not None else None,
    })


def load_checkpoints(root, manifest, cases, fingerprints):
    rows = {}
    for path in sorted((root / "checkpoints").glob("*/*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        row = payload["row"]
        key = row["instance_id"], row["solver"]
        if (key in rows or key[0] not in cases or key[1] not in manifest["solvers"]
                or payload["configuration_digest"] != manifest["configuration_digest"]
                or payload["row_digest"] != digest(row)
                or row["timeout_s"] != manifest["timeout_s"]
                or payload["instance_digest"] != cases[key[0]]
                or row["solver_source_sha256"] != fingerprints[key[1]]
                or path != root / "checkpoints" / key[1] / (key[0] + ".json")):
            raise ValueError(f"invalid checkpoint or budget: {path}")
        validate_results([row], {"instance_ids": [key[0]], "solvers": {key[1]: None}})
        if row["status"] == "solved" and not row["plan_path"]:
            raise ValueError(f"checkpoint lost its solved trace: {path}")
        if row["plan_path"]:
            plan = inside_run(root, row["plan_path"])
            if not plan.is_file() or file_hash(plan) != payload["plan_sha256"]:
                raise ValueError(f"checkpoint trace changed or missing: {path}")
        rows[key] = row
    return rows
