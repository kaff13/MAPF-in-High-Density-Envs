import unittest
from research.detour.solver import DetourPHANS

class ChoiceTests(unittest.TestCase):
    def planner(self,walls,enabled=True):
        p=DetourPHANS(4,3,static_obstacles=walls,detour_enabled=enabled)
        p.task_len=0;p.ag_cur_pos_lst=[];p.tgt_ag_path_lst=[];p.tgt_cur_steps=[]
        return p
    def test_original_tie_survives_when_manhattan_is_attainable(self):
        self.assertEqual(self.planner([])._choose_null_position((0,0),[(2,0),(0,2)],{}),(2,0))
    def test_wall_triggers_alternative_and_control_retains_original(self):
        self.assertEqual(self.planner([(1,0)])._choose_null_position((0,0),[(2,0),(0,2)],{}),(0,2))
        self.assertEqual(self.planner([(1,0)],False)._choose_null_position((0,0),[(2,0),(0,2)],{}),(2,0))
