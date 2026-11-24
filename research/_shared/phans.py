"""Default-preserving scaffold copied from pinned original PHANS.

Hooks expose blocker order/window, vacancy choice and phase continuation.
Defaults retain all blockers, original NumPy assignment and one-progress
execution phases. No optimized search/copy or retiming is enabled here.
Original run_loop derives from a82ed819d37932ff845e170805f41e24c82e550b.
"""

# Copyright (C) 2025 TOYOTA CENTRAL R&D LABS., INC. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (collectively, the "Software"), the rights to use, copy,
# modify and/or merge the Software, for non-commercial research purposes, specifically limited
# to educational use, verification of research results, publication in academic papers, and
# presentations at academic conferences, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# Except as expressly stated herein, no rights or licenses from any copyright holder are granted,
# whether expressly, by implication, estoppel or otherwise.
#
# The name and trademarks of copyright holder(s) may NOT be used in advertising or publicity
# pertaining to the Software or portions thereof including modifications or derivatives, without
# specific written prior permission. Title to copyright in the Software will at all times remain
# with the copyright holders.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import copy

import numpy as np

from solver.a_star import AStarFollowingConflict
from solver.phans_null_agent_swapping import PHANS


class ExperimentalPHANS(PHANS):
    def __init__(self, size_x, size_y, static_obstacles=None, *, lookahead=None):
        if lookahead is not None and (type(lookahead) is not int or lookahead < 1):
            raise ValueError("lookahead must be a positive integer or None")
        super().__init__(size_x, size_y, static_obstacles=static_obstacles)
        self.lookahead = lookahead

    def _blocker_limit(self, target_index):
        return self.lookahead

    def _order_blockers(self, positions, distances):
        # Keep the original stable priority and allow isolated scheduling ablations.
        return [pos for _, pos in sorted(zip(distances, positions),
                                         key=lambda item: item[0], reverse=True)]

    def _continue_phase(self, target_moved, phase_ticks, null_paths):
        # Default PHANS replans immediately after the first target advance.
        return not target_moved

    def _choose_null_position(self, bag_pos, candidates, penalties):
        # Original PHANS calculation, extracted without changing NumPy or ties.
        dst_penalty_array = np.array([penalties.get(pos, 0) for pos in candidates])
        distances = np.abs(np.array(candidates) - np.array(bag_pos)).sum(axis=1) + dst_penalty_array
        min_index = np.argmin(distances)
        return candidates[min_index]

    def _select_null_agents(self, blocking_ag_pos_lst, tgt_ags_cur_pos_lst):
        # Choose the empty vertices
        self._update_null_ag_pos_lst()
        available_null_ags_pos_lst = copy.deepcopy(list(set(self.null_ag_pos_lst)))
        selected_null_ags_pos_lst = []

        for i, bag_pos in enumerate(blocking_ag_pos_lst):
            # Generally choose the null agent with the smallest h-value,
            # but avoid interfering with target agents' movements.

            dst_from_bag_to_goal = float("inf")
            for i_tgt_ag in range(self.task_len):
                if bag_pos in self.tgt_ag_path_lst[i_tgt_ag]:
                    dst_from_bag_to_goal = min(
                        dst_from_bag_to_goal,
                        len(self.tgt_ag_path_lst[i_tgt_ag])
                        - self.tgt_ag_path_lst[i_tgt_ag].index(bag_pos)
                        - 1,
                    )

            # Preserve vertices between the target and obstructing agents on target paths
            tgt_preserved_pos = []
            dst_penalty_dct = {}

            for i_tgt_ag in range(self.task_len):
                tgt_idx_on_tgt_ag_path = self.tgt_cur_steps[i_tgt_ag]

                if bag_pos in self.tgt_ag_path_lst[i_tgt_ag]:
                    bag_idx_on_tgt_ag_path = self.tgt_ag_path_lst[i_tgt_ag].index(bag_pos)
                    for pos in self.tgt_ag_path_lst[i_tgt_ag][bag_idx_on_tgt_ag_path:]:
                        dst_from_null_to_tgt = np.sum(
                            np.abs(np.array(pos) 
                                   - np.array(self.tgt_ag_path_lst[i_tgt_ag]\
                                       [self.tgt_cur_steps[i_tgt_ag]])
                            )
                        )
                        if pos in dst_penalty_dct.keys():
                            dst_penalty_dct[pos] = max(
                                dst_penalty_dct[pos],                        
                                dst_from_null_to_tgt
                            )
                        else:
                            dst_penalty_dct[pos] = dst_from_null_to_tgt
                            
                # For null agents from the target's current position to the goal:
                for pos in self.tgt_ag_path_lst[i_tgt_ag][tgt_idx_on_tgt_ag_path:]:
                    dst_to_goal = (
                        len(self.tgt_ag_path_lst[i_tgt_ag])
                        - self.tgt_ag_path_lst[i_tgt_ag].index(pos)
                        - 1
                    )
                    if dst_from_bag_to_goal < dst_to_goal:
                        tgt_preserved_pos.append(pos)

            tmp_available_null_ags_pos_lst = [
                null_ag_pos
                for null_ag_pos in available_null_ags_pos_lst
                if null_ag_pos not in tgt_preserved_pos
            ]

            if len(tmp_available_null_ags_pos_lst) > 0:
                pos = self._choose_null_position(bag_pos, tmp_available_null_ags_pos_lst, dst_penalty_dct)
                selected_null_ags_pos_lst.append(pos)
                available_null_ags_pos_lst.remove(pos)
            else:
                break

        return selected_null_ags_pos_lst

    def run_loop(
        self, 
        ag_start_pos_lst: list[tuple[int, int]], 
        task_lst: list[tuple[int, int]], 
        a_star_max_iter: int = -1, 
        max_loop: int = 300
    ) -> list[list[tuple[int, int]]]:
        """
        Move agents step-by-step following the target paths.

        This loop:
        - Advances target agents along their target paths.
        - Detects following conflicts (including edge conflicts) and vertex
          conflicts against agents that already reached their goals.
        - Identifies obstructing agents and moves null agents to vacate those cells.
        """
        # -----------------------------------
        # 1. Plan target paths
        # -----------------------------------
        self._init_loop(ag_start_pos_lst, task_lst, a_star_max_iter)

        # -----------------------------------
        # 2. Evacuate obstructing agents and move target agents
        # -----------------------------------
        
        # Initialize
        all_path_lst = [copy.deepcopy(self.ag_cur_pos_lst)]
        self.tgt_cur_steps = [0] * len(self.tgt_ag_path_lst)

        loop = 0
        self._update_goal_ag()
        tgt_ags_cur_pos_lst = self.ag_cur_pos_lst[: self.task_len]
        
        for i_tgt_ag in [i for i in range(self.task_len) if i not in self.goal_ag_idx_lst]:
            self.tgt_cur_steps[i_tgt_ag] = (
                len(self.tgt_ag_path_lst[i_tgt_ag])
                - self.tgt_ag_path_lst[i_tgt_ag][::-1].index(tgt_ags_cur_pos_lst[i_tgt_ag])
                - 1
            )

        # Start loop
        while (
            any(
                self.tgt_cur_steps[i] < len(self.tgt_ag_path_lst[i]) - 1
                for i in range(self.task_len)
            )
            and loop < max_loop
        ):
            # Identify obstructing agents
            
            # next blocking agents on target paths
            blocking_ag_pos_lst = [] 
            # their remaining distance along the blocked target’s path to its goal
            next_blocking_ag_dist_from_goal_lst = []

            for i_tgt_ag in range(self.task_len):
                if self.tgt_cur_steps[i_tgt_ag] < len(self.tgt_ag_path_lst[i_tgt_ag]) - 1:
                    next_tgt_pos_lst = self.tgt_ag_path_lst[i_tgt_ag][
                        self.tgt_cur_steps[i_tgt_ag] + 1 :
                    ]

                    # Get the next blocking agent position
                    path_blockers = set()
                    blocker_limit = self._blocker_limit(i_tgt_ag)
                    for pos in next_tgt_pos_lst:
                        if pos in self.ag_cur_pos_lst and pos not in tgt_ags_cur_pos_lst:
                            path_blockers.add(pos)
                            if blocker_limit is not None and len(path_blockers) > blocker_limit:
                                break
                            dst_to_goal = (
                                len(self.tgt_ag_path_lst[i_tgt_ag])
                                - self.tgt_ag_path_lst[i_tgt_ag].index(pos)
                                + 1
                            )
                            if pos not in blocking_ag_pos_lst:
                                blocking_ag_pos_lst.append(pos)
                                next_blocking_ag_dist_from_goal_lst.append(dst_to_goal)
                            else:
                                idx = blocking_ag_pos_lst.index(pos)
                                if next_blocking_ag_dist_from_goal_lst[idx] < dst_to_goal:
                                    # If multiple target agents share the same blocker,
                                    # increase its priority by updating with the larger distance.
                                    next_blocking_ag_dist_from_goal_lst[idx] = dst_to_goal

            # Order the obstructing agents
            blocking_ag_pos_lst = self._order_blockers(
                blocking_ag_pos_lst, next_blocking_ag_dist_from_goal_lst
            )

            # Define dependency among target agents:
            # If a target agent appears earlier on another's path, move the earlier one first.
            high_priority_blocking_ag_pos_lst = []
            dependency_relation = []  # (A, B): A depends on B

            for i_tgt_ag in [i for i in range(self.task_len) if i not in self.goal_ag_idx_lst]:
                tgt_ag_next_pos = self.tgt_ag_path_lst[i_tgt_ag][self.tgt_cur_steps[i_tgt_ag] + 1]
                tgt_ag_cur_idx = self.tgt_cur_steps[i_tgt_ag]

                for j_tgt_ag in range(self.task_len):
                    if i_tgt_ag != j_tgt_ag:
                        from_idx = self.tgt_cur_steps[j_tgt_ag]
                        to_idx = min(len(self.tgt_ag_path_lst[j_tgt_ag]) - 1, tgt_ag_cur_idx)
                        if tgt_ag_next_pos in self.tgt_ag_path_lst[j_tgt_ag][from_idx:to_idx]:
                            if j_tgt_ag in [x for x, _ in dependency_relation]:
                                dependency_relation.append((i_tgt_ag, j_tgt_ag))
                            else:
                                dependency_relation = [(i_tgt_ag, j_tgt_ag)] + dependency_relation

            for i_tgt_ag, j_tgt_ag in dependency_relation:
                tgt_ag_next_pos = self.tgt_ag_path_lst[i_tgt_ag][self.tgt_cur_steps[i_tgt_ag] + 1]
                from_idx = self.tgt_cur_steps[j_tgt_ag]
                high_priority_blocking_ag_pos_lst += self.tgt_ag_path_lst[j_tgt_ag][
                    from_idx : min(
                        len(self.tgt_ag_path_lst[j_tgt_ag]),
                        self.tgt_ag_path_lst[j_tgt_ag].index(tgt_ag_next_pos) + 2,
                    )
                ][::-1]

            for pos in high_priority_blocking_ag_pos_lst:
                if pos in blocking_ag_pos_lst:
                    blocking_ag_pos_lst.remove(pos)
                    blocking_ag_pos_lst = [pos] + blocking_ag_pos_lst

            selected_null_ags_pos_lst = self._select_null_agents(
                blocking_ag_pos_lst, tgt_ags_cur_pos_lst
            )

            # Plan paths for null agents to move to obstructing agents' positions.
            dimension = (self.size_x, self.size_y)
            obss = self.static_obss + list(
                set(tgt_ags_cur_pos_lst)
                - set(selected_null_ags_pos_lst)
                - set(blocking_ag_pos_lst)
            )
            ags = []
            for i in range(len(selected_null_ags_pos_lst)):
                if len(ags) == 0 or blocking_ag_pos_lst[i] not in [ag["goal"] for ag in ags]:
                    ags.append(
                        {
                            "start": selected_null_ags_pos_lst[i],
                            "goal": blocking_ag_pos_lst[i],
                            "name": i,
                        }
                    )

            mov_obss = []
            solution_dict_all = []
            for ag in ags:
                tgt_preserved_pos = []
                for i_tgt_ag in range(self.task_len):
                    if ag["goal"] in self.tgt_ag_path_lst[i_tgt_ag]:
                        tgt_preserved_pos += [
                            pos
                            for pos in self.tgt_ag_path_lst[i_tgt_ag][
                                self.tgt_cur_steps[i_tgt_ag] : self.tgt_ag_path_lst[
                                    i_tgt_ag
                                ].index(ag["goal"])
                            ]
                        ]

                env = AStarFollowingConflict(
                    dimension,
                    ag,
                    set(obss + tgt_preserved_pos),
                    moving_obstacles=mov_obss,
                    moving_obstacle_edges=[],
                    a_star_max_iter=10000,
                    is_dst_add=False,
                )
                solution = env.compute_solution()
                mov_obss += [(s["x"], s["y"], s["t"]) for s in solution]
                solution_dict_all.append(solution)

            null_ags_path_lst = []
            for solution_dict in solution_dict_all:
                null_ags_path_lst.append([(s['x'], s['y']) for s in solution_dict])

            # Execute movements
            ag_next_pos_lst = copy.deepcopy(self.ag_cur_pos_lst)
            ag_pre_pos_lst = []

            one_tgt_ag_goal_flag = True
            phase_ticks = 0
            while one_tgt_ag_goal_flag and loop < max_loop:
                one_tgt_ag_goal_flag = True
                ag_pre_pos_lst = []
                # Move target agents if possible
                for i_tgt_ag in [
                    i for i in range(self.task_len) if i not in self.goal_ag_idx_lst
                ]:
                    tgt_ag_next_pos = self.tgt_ag_path_lst[i_tgt_ag][
                        self.tgt_cur_steps[i_tgt_ag] + 1
                    ]
                    if (
                        tgt_ag_next_pos not in ag_next_pos_lst
                        and tgt_ag_next_pos not in ag_pre_pos_lst
                    ):
                        ag_pre_pos_lst.append(copy.deepcopy(ag_next_pos_lst[i_tgt_ag]))
                        ag_next_pos_lst[i_tgt_ag] = copy.deepcopy(tgt_ag_next_pos)
                        one_tgt_ag_goal_flag = False

                # Move null agents by one step if possible
                for i_null_ag in range(len(null_ags_path_lst)):
                    if len(null_ags_path_lst[i_null_ag]) > 1:
                        # null_ag_pos_idx_lst_on_null_ag_path: 
                        #   indices where the null agent can be on its path.
                        #   Typically 0, but due to Manhattan distance selection,
                        #   it may differ (if it wasn't the nearest one).
                        null_ag_pos_idx_lst_on_null_ag_path = [
                            i
                            for i, pos in enumerate(null_ags_path_lst[i_null_ag])
                            if pos not in self.ag_cur_pos_lst[self.task_len:]
                            and pos not in ag_next_pos_lst[self.task_len:]
                        ]

                        if len(null_ag_pos_idx_lst_on_null_ag_path) > 0:
                            null_ag_cur_pos_idx = max(null_ag_pos_idx_lst_on_null_ag_path)
                            null_ag_cur_pos = null_ags_path_lst[i_null_ag][null_ag_cur_pos_idx]

                            if (
                                null_ag_cur_pos not in ag_next_pos_lst
                                and null_ag_cur_pos_idx < len(null_ags_path_lst[i_null_ag]) - 1
                            ):
                                null_ag_next_pos = null_ags_path_lst[i_null_ag][
                                    null_ag_cur_pos_idx + 1
                                ]

                                # Move a null agent by swapping with the adjacent agent:
                                #   |■|□|  -->  |□|■|
                                if (
                                    null_ag_next_pos in self.ag_cur_pos_lst
                                    and null_ag_next_pos in ag_next_pos_lst
                                ):
                                    ag_next_pos_lst[
                                        ag_next_pos_lst.index(null_ag_next_pos)
                                    ] = copy.deepcopy(null_ag_cur_pos)
                                    null_ags_path_lst[i_null_ag] = null_ags_path_lst[i_null_ag][1:]

                print(ag_next_pos_lst[: self.task_len])
                self.tgt_ag_path_lst_plot.append(copy.deepcopy(self.tgt_ag_path_lst))
                all_path_lst.append(copy.deepcopy(ag_next_pos_lst))
                self.ag_cur_pos_lst = copy.deepcopy(ag_next_pos_lst)

                loop += 1
                phase_ticks += 1
                one_tgt_ag_goal_flag = self._continue_phase(
                    not one_tgt_ag_goal_flag, phase_ticks, null_ags_path_lst
                )

            self._update_goal_ag()
            tgt_ags_cur_pos_lst = self.ag_cur_pos_lst[: self.task_len]
            for i_tgt_ag in [i for i in range(self.task_len) if i not in self.goal_ag_idx_lst]:
                self.tgt_cur_steps[i_tgt_ag] = (
                    len(self.tgt_ag_path_lst[i_tgt_ag])
                    - self.tgt_ag_path_lst[i_tgt_ag][::-1].index(
                        tgt_ags_cur_pos_lst[i_tgt_ag]
                    )
                    - 1
                )
            self._update_goal_ag()

        return all_path_lst

