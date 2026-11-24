"""Correctness fixtures, not performance benchmark results."""
from contextlib import redirect_stdout
from io import StringIO
import importlib
import json
from pathlib import Path
import unittest

from benchmark.maps import GridMap, Instance
from benchmark.validation import check_trace

def case():
    grid=GridMap('dossier-unit',8,5,frozenset(),((7,0),(7,4)))
    return Instance('dossier-unit',grid,((0,0),(0,4),(1,0),(2,0),(4,0),(1,4),(2,4),(4,4),(3,2)),23,0)

class DossierTests(unittest.TestCase):
    def test_canonical_solver_returns_valid_complete_trace(self):
        solver=importlib.import_module('research.blocker_window.solver')
        instance=case()
        with redirect_stdout(StringIO()):
            trace=solver.solve(instance)
        self.assertEqual(check_trace(instance,trace).status,'solved')

    def test_implementation_imports_only_its_own_family_or_shared_scaffold(self):
        import ast
        folder=Path(__file__).resolve().parents[1]
        for file in folder.glob('*.py'):
            for node in ast.walk(ast.parse(file.read_text(encoding='utf-8'))):
                modules=([node.module] if isinstance(node,ast.ImportFrom) and node.level==0
                         else [a.name for a in node.names] if isinstance(node,ast.Import) else [])
                for module in modules:
                    if module and module.startswith('research.'):
                        self.assertTrue(module.startswith(('research.blocker_window.','research._shared.')), (file,module))
