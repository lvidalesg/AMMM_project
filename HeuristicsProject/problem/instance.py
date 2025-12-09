"""
AMMM Lab Heuristics
Representation of a problem instance
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

from HeuristicsProject.problem.Crossing import Crossing
from HeuristicsProject.problem.Camera import Camera
from HeuristicsProject.problem.solution import Solution


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        K = inputData.K  # number of cameras
        N = inputData.N  # number of crossroads
        P = inputData.P  # price
        R = inputData.R  # range
        A = inputData.A  # autonomy
        C = inputData.C  # cost
        self.M = inputData.M  # distance matrix

        self.crossings = [None] * N  # vector with crossings
        for nId in range(0, N):  # nId = 0..(N-1)
            self.crossings[nId] = Crossing(nId)

        self.cameras = [None] * K  # vector with cameras
        for kId in range(0, K):  # kId = 0..(K-1)
            self.cameras[kId] = Camera(kId, P[kId], R[kId], A[kId], C[kId])

    def getNumCrossings(self):
        return len(self.crossings)

    def getNumCameras(self):
        return len(self.cameras)

    def getCrossings(self):
        return self.crossings

    def getCameras(self):
        return self.cameras

    def getDistanceMatrix(self):
        return self.M

    def createSolution(self):
        solution = Solution(self.crossings, self.cameras, self.M)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        # Check if there are enough cameras to potentially cover all crossings
        # This is a basic feasibility check
        return len(self.cameras) > 0 and len(self.crossings) > 0
