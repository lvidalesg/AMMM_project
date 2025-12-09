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
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):
        # sort candidates by score (cost per new coverage)
        sortedCandidateList = sorted(candidateList, key=lambda x: x['score'])

        minScore = sortedCandidateList[0]['score']
        maxScore = sortedCandidateList[-1]['score']
        boundaryScore = minScore + (maxScore - minScore) * alpha

        rcl = [c for c in sortedCandidateList if c['score'] <= boundaryScore]
        if not rcl:
            return None
        return random.choice(rcl)
    
    def _greedyRandomizedConstruction(self, alpha):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        cameras = self.instance.getCameras()

        for camera in cameras:
            cameraId = camera.getId()

            candidateList = solution.computeCandidates(cameraId)

            if not candidateList:
                continue

            candidate = self._selectCandidate(candidateList, alpha)
            if candidate is None:
                continue

            solution.assign(cameraId, candidate['crossingId'])
            solution.cameraIdToPattern[cameraId] = candidate['pattern']
        
        return solution
    
    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestHighestLoad = incumbent.getFitness()
        self.writeLogLine(bestHighestLoad, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1
            
            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self._greedyRandomizedConstruction(alpha)
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            if solution.isFeasible():
                solutionHighestLoad = solution.getFitness()
                if solutionHighestLoad < bestHighestLoad :
                    incumbent = solution
                    bestHighestLoad = solutionHighestLoad
                    self.writeLogLine(bestHighestLoad, iteration)

        self.writeLogLine(bestHighestLoad, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

