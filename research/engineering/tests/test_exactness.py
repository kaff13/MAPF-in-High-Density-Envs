from contextlib import redirect_stdout
from io import StringIO
import unittest
from .test_solver import case
from research._shared.runtime import solve_planner
from research.engineering.solver import solve,indexed,indexed_copy,tuple_only

class ExactnessTests(unittest.TestCase):
    def test_optimized_stages_preserve_complete_raw_trace(self):
        instance=case()
        with redirect_stdout(StringIO()):
            expected=solve_planner(instance)
            for candidate in (indexed,indexed_copy,tuple_only,solve):
                self.assertEqual(candidate(instance),expected,candidate.__name__)
