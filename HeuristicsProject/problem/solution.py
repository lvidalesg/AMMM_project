"""
AMMM Lab Heuristics
Representation of a solution instance
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

from itertools import product
from HeuristicsProject.solution import _Solution


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    DAYS = 7

    def __init__(self, crossings, cameras, distanceMatrix):
        self.crossings = crossings
        self.cameras = cameras  # camera models (can be reused)
        self.M = distanceMatrix
        # Each assignment is a tuple (modelId, crossingId, pattern)
        self.assignments = []  # list of (modelId, crossingId, pattern) tuples
        self.usedCrossings = set()  # crossings that already have a camera
        # Covered universe are pairs (crossingId, day)
        self.coveredCrossingDays = set()
        super().__init__()


    @staticmethod
    def isPatternValid(pattern, A_k):
        """Validate circular runs of 1s: each run length in [2, A_k]."""
        if sum(pattern) == 0:
            return False
        runs = []
        cur = 0
        for b in pattern:
            if b == 1:
                cur += 1
            else:
                if cur > 0:
                    runs.append(cur)
                cur = 0
        if cur > 0:
            runs.append(cur)
        if pattern[0] == 1 and pattern[-1] == 1 and len(runs) >= 2:
            merged = runs[0] + runs[-1]
            runs = [merged] + runs[1:-1] if len(runs) > 2 else [merged]
        for r in runs:
            if r < 2 or r > A_k:
                return False
        return True

    @staticmethod
    def getAllValidPatterns(A_k):
        """Return list of valid patterns for autonomy A_k."""
        patterns = []
        for bits in product([0, 1], repeat=7):
            if Solution.isPatternValid(bits, A_k):
                patterns.append(bits)
        return patterns

    def calculateFitness(self):
        # Objective (fitness) = total weekly cost
        # For each assignment: P_k + days_on * C_k where days_on = sum(pattern)
        totalCost = 0.0
        for modelId, crossingId, pattern in self.assignments:
            cam = self.cameras[modelId]
            days_on = sum(pattern)
            totalCost += cam.getPrice() + days_on * cam.getCost()
        self.fitness = totalCost
        return self.fitness

    def updateCoverage(self):
        """
        Recalculate covered crossing-day pairs based on current assignments.
        """
        self.coveredCrossingDays.clear()

        for modelId, crossingId, pattern in self.assignments:
            camera = self.cameras[modelId]
            cameraRange = camera.getRange()

            for crossing in self.crossings:
                targetCrossingId = crossing.getId()
                distance = self.M[crossingId][targetCrossingId]
                if distance <= cameraRange:
                    for day in range(self.DAYS):
                        if pattern[day] == 1:
                            self.coveredCrossingDays.add((targetCrossingId, day))

    def assign(self, modelId, crossingId, pattern):
        """Add a new camera assignment (model can be reused, but crossing cannot)"""
        if crossingId in self.usedCrossings:
            return False  # crossing already has a camera
        
        self.assignments.append((modelId, crossingId, pattern))
        self.usedCrossings.add(crossingId)
        self.updateCoverage()
        self.calculateFitness()
        return True
    
    def _computeCost(self, modelId, pattern):
        camera = self.cameras[modelId]
        price = camera.getPrice()
        cost = camera.getCost()
        days_on = sum(pattern)
        return price + days_on * cost

    def computeCandidates(self):
        """
        Returns list of candidate plans:
        each candidate is a dict with keys:
        - 'modelId': camera model (0-based, can be reused)
        - 'crossingId': location (0-based)
        - 'pattern': tuple of 7 bits
        - 'cost': P_k + days_on * C_k
        - 'covered': set of (node, day) pairs (0-based)
        """
        candidates = []
        
        for modelId in range(len(self.cameras)):
            for crossingId in range(len(self.crossings)):
                validPatterns = self.getAllValidPatterns(self.cameras[modelId].getAutonomy())
                for pattern in validPatterns:
                    # Compute cost for this triplet
                    cost = self._computeCost(modelId, pattern)
                    covered = set()
                    for d, is_on in enumerate(pattern):
                        if is_on == 1:
                            covered |= {(j, d) for j in range(len(self.crossings)) if self.M[crossingId][j] <= self.cameras[modelId].getRange()}
                    if covered:                  
                        candidates.append({
                            'modelId': modelId,
                            'crossingId': crossingId,
                            'pattern': pattern,
                            'cost': cost,
                            'covered': covered
                        })
            
        return candidates
    
    def selectBestCandidate(self, candidates):
        """
        Select the best candidate (minimum q = cost / new_coverage).
        Models can be reused, but crossings cannot (one camera per crossing max).
        Returns the candidate dict with lowest score, or None if no valid candidate.
        """
        best = None
        best_score = float('inf')
        
        for cand in candidates:
            # Skip if crossing already has a camera
            if cand['crossingId'] in self.usedCrossings:
                continue
            
            # Compute newly covered crossing-day pairs
            new_cov = cand['covered'] - self.coveredCrossingDays
            new_count = len(new_cov)
            
            if new_count == 0:
                continue
            
            # Score: q = cost / newly_covered
            score = cand['cost'] / new_count
            
            if score < best_score:
                best_score = score
                best = cand
        
        return best
    
    def greedyConstruction(self):
        """
        Execute complete greedy construction: iteratively select best candidates
        until all crossing-day pairs are covered or no more improvements possible.
        Models can be reused, so we don't remove candidates after selection.
        """
        # Compute all candidate triplets once
        candidates = self.computeCandidates()
        
        universeSize = len(self.crossings) * self.DAYS
        
        # Greedy set cover loop
        while len(self.coveredCrossingDays) < universeSize:
            # Select best candidate
            best = self.selectBestCandidate(candidates)
            
            if best is None:
                break  # No more candidates can improve coverage
            
            # Assign the camera model with selected pattern
            modelId = best['modelId']
            crossingId = best['crossingId']
            pattern = best['pattern']
            self.assign(modelId, crossingId, pattern)
        
        return self

    def __str__(self):
        strSolution = 'z = %10.2f;\n' % self.fitness
        covered = len(self.coveredCrossingDays)
        total = len(self.crossings) * self.DAYS
        strSolution += 'Covered crossing-day pairs: %d / %d\n' % (covered, total)
        if self.fitness == float('-inf'):
            return strSolution

        # Print assignments as list
        strSolution += 'Assignments (modelId, crossingId, pattern):\n'
        for modelId, crossingId, pattern in self.assignments:
            strSolution += f'  Model {modelId} -> Crossing {crossingId}, Pattern: {pattern}\n'

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
