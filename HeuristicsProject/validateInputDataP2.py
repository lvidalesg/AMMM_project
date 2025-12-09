"""
AMMM Lab Heuristics
Instance file validator v2.0
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

from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['K', 'N', 'P', 'R', 'A', 'C', 'M']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate K (number of cameras)
        K = data.K
        if not isinstance(K, int) or (K <= 0):
            raise AMMMException('K(%s) has to be a positive integer value.' % str(K))

        # Validate N (number of crossroads)
        N = data.N
        if not isinstance(N, int) or (N <= 0):
            raise AMMMException('N(%s) has to be a positive integer value.' % str(N))

        # Validate P (price of cameras)
        data.P = list(data.P)
        P = data.P
        if len(P) != K:
            raise AMMMException('Size of P(%d) does not match with value of K(%d).' % (len(P), K))

        for value in P:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException('Invalid parameter value(%s) in P. Should be a number greater or equal than zero.' % str(value))

        # Validate R (range of cameras)
        data.R = list(data.R)
        R = data.R
        if len(R) != K:
            raise AMMMException('Size of R(%d) does not match with value of K(%d).' % (len(R), K))

        for value in R:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException('Invalid parameter value(%s) in R. Should be a number greater or equal than zero.' % str(value))

        # Validate A (autonomy of cameras)
        data.A = list(data.A)
        A = data.A
        if len(A) != K:
            raise AMMMException('Size of A(%d) does not match with value of K(%d).' % (len(A), K))

        for value in A:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException('Invalid parameter value(%s) in A. Should be a number greater or equal than zero.' % str(value))

        # Validate C (cost of cameras)
        data.C = list(data.C)
        C = data.C
        if len(C) != K:
            raise AMMMException('Size of C(%d) does not match with value of K(%d).' % (len(C), K))

        for value in C:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException('Invalid parameter value(%s) in C. Should be a number greater or equal than zero.' % str(value))

        # Validate M (distance matrix between crossroads)
        data.M = [list(row) for row in data.M]
        M = data.M
        if len(M) != N:
            raise AMMMException('Number of rows in M(%d) does not match with value of N(%d).' % (len(M), N))

        for i, row in enumerate(M):
            if len(row) != N:
                raise AMMMException('Number of columns in M row %d (%d) does not match with value of N(%d).' % (i, len(row), N))
            
            for j, value in enumerate(row):
                if not isinstance(value, (int, float)) or (value < 0):
                    raise AMMMException('Invalid parameter value(%s) in M[%d][%d]. Should be a number greater or equal than zero.' % (str(value), i, j))
                
                # Validate diagonal is zero
                if i == j and value != 0:
                    raise AMMMException('Diagonal element M[%d][%d] should be zero, but is %s.' % (i, j, str(value)))

