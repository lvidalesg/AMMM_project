'''
AMMM Lab Heuristics
GRASP solver
Copyright 2018 Luis Velasco.

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
'''

import random
import time
from HeuristicsProject.solver import _Solver
from HeuristicsProject.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _greedyRandomizedConstruction(self, candidates, alpha, solution, universeSize):
        """
        Greedy randomized construction with RCL selection.
        alpha=0 => pure greedy, alpha=1 => pure random
        Selects one random candidate from RCL per iteration and accepts it.
        """
        while len(solution.coveredCrossingDays) < universeSize:
            # Get available candidates (not yet assigned crossings)
            available = [c for c in candidates if c['crossingId'] not in solution.usedCrossings]
            
            if not available:
                break
            
            # Compute scores for available candidates
            scored = []
            for cand in available:
                new_cov = cand['covered'] - solution.coveredCrossingDays
                new_count = len(new_cov)
                if new_count > 0:
                    score = cand['cost'] / new_count
                    scored.append((score, cand))
            
            if not scored:
                break
            
            # Sort by score
            scored.sort(key=lambda x: x[0])
            q_min = scored[0][0]
            q_max = scored[-1][0]
            
            # Build RCL
            threshold = q_min + alpha * (q_max - q_min)
            rcl = [cand for score, cand in scored if score <= threshold]
            
            if not rcl:
                break
            
            # Select randomly from RCL and assign immediately
            best = random.choice(rcl)
            solution.assign(best['modelId'], best['crossingId'], best['pattern'])
    
    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        
        # Pre-compute candidates once
        tempSolution = self.instance.createSolution()
        allCandidates = tempSolution.computeCandidates()
        universeSize = len(tempSolution.crossings) * tempSolution.DAYS
        
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestFitness = incumbent.getFitness()
        self.writeLogLine(bestFitness, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1
            
            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self.instance.createSolution()
            candidates = list(allCandidates)  # copy list for this iteration
            
            self._greedyRandomizedConstruction(candidates, alpha, solution, universeSize)
            print(f"Iter {iteration}: alpha={alpha:.2f}, before_LS: fitness={solution.getFitness():.2f}")
            
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)
                print(f"Iter {iteration}: after_LS: fitness={solution.getFitness():.2f}")

            if solution.isFeasible():
                solutionFitness = solution.getFitness()
                if solutionFitness < bestFitness:
                    incumbent = solution
                    bestFitness = solutionFitness
                    self.writeLogLine(bestFitness, iteration)

        self.writeLogLine(bestFitness, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

