"""Discover standalone research tests without documentation or metadata files."""
from pathlib import Path
import unittest


def load_tests(loader, standard_tests, pattern):
    root = Path(__file__).resolve().parents[1]
    for folder in sorted((root / "research").glob("*/tests")):
        if not (folder.parent / "solver.py").is_file():
            continue
        standard_tests.addTests(unittest.TestLoader().discover(
            str(folder), pattern="test_*.py", top_level_dir=str(root)))
    return standard_tests
