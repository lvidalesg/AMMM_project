"""
AMMM Lab Heuristics
Local Search algorithm for Camera Coverage Problem
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy
import time
from HeuristicsProject.solver import _Solver
from AMMMGlobals import AMMMException


class LocalSearch(_Solver):
    """Greedy constructive + Local Search using only redundancy removal."""

    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.maxExecTime = config.maxExecTime
        self.deadline = None
        super().__init__(config, instance)

    # ------------------------------------------------------------------
    # Helper utilities
    # ------------------------------------------------------------------
    @staticmethod
    def _universe_size(solution):
        return len(solution.crossings) * solution.DAYS

    @staticmethod
    def _has_full_coverage(solution, universe_size):
        return len(solution.coveredCrossingDays) == universe_size

    # ------------------------------------------------------------------
    # Neighborhood move
    # ------------------------------------------------------------------
    def _remove_redundant_camera(self, solution, universe_size, current_cost):
        for idx in range(len(solution.assignments)):
            model_id, crossing_id, pattern = solution.assignments[idx]
            removed_assignment = solution.assignments.pop(idx)
            solution.usedCrossings.remove(crossing_id)
            solution.updateCoverage()
            new_cost = solution.calculateFitness()

            if self._has_full_coverage(solution, universe_size) and new_cost < current_cost:
                return True

            # revert removal
            solution.assignments.insert(idx, removed_assignment)
            solution.usedCrossings.add(crossing_id)
            solution.updateCoverage()
            solution.calculateFitness()

            if time.time() >= self.deadline:
                break

        return False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def solve(self, **kwargs):
        initial_solution = kwargs.get('solution', None)
        if initial_solution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initial_solution.isFeasible():
            return initial_solution

        start_time = kwargs.get('startTime', time.time())
        end_time = kwargs.get('endTime', start_time + self.maxExecTime)
        self.deadline = end_time

        current_solution = copy.deepcopy(initial_solution)
        current_solution.updateCoverage()
        current_solution.calculateFitness()

        universe_size = self._universe_size(current_solution)
        if not self._has_full_coverage(current_solution, universe_size):
            return current_solution

        improved = True
        while improved and time.time() < self.deadline:
            improved = False
            current_cost = current_solution.getFitness()

            if self._remove_redundant_camera(current_solution, universe_size, current_cost):
                improved = True

        return current_solution
