from itertools import product
from load_data_python import load_dat_file
from math import inf
from pathlib import Path
import random
import argparse

DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

class CameraSystem:

    def __init__(self, K, P, R, A, C, N, M):
        self.K = K
        self.P = P
        self.R = R
        self.A = A
        self.C = C
        self.N = N
        self.M = M

    def isPatternValid(self, pattern, A_k):
        """pattern: tuple of 7 bits (0/1). Validate circular runs of 1s: each run length in [2, A_k]."""
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
        # if pattern starts and ends with 1, merge first and last (circular)
        if pattern[0] == 1 and pattern[-1] == 1 and len(runs) >= 2:
            # first run is runs[0] (prefix), last run is runs[-1] (suffix)
            merged = runs[0] + runs[-1]
            # replace
            runs = [merged] + runs[1:-1] if len(runs) > 2 else [merged]
        # check each run's length bounds
        for r in runs:
            if r < 2 or r > A_k:
                return False
        return True

    def getAllValidPatterns(self, A_k):
        """Return list of patterns (tuples) valid for autonomy A_k."""
        patterns = []
        for bits in product([0,1], repeat=7):
            if self.isPatternValid(bits, A_k):
                patterns.append(bits)
        return patterns
    
    def computeCost(self, pattern, P_k, C_k):
        days_on = sum(pattern)
        return P_k + days_on * C_k

    def computeCandidates(self):
        """
        Returns list of candidate plans:
        each candidate is a dict with keys:
        - 'i': location (0-based)
        - 'k': model (0-based)
        - 'pattern': tuple of 7 bits
        - 'cost': P_k + days_on * C_k
        - 'covered': set of (node, day) pairs (0-based)
        """
        candidates = []
        for i in range(self.N):
            for k in range(self.K):
                patterns = self.getAllValidPatterns(self.A[k])
                # If no valid pattern exists for this A[k], continue (shouldn't happen with A>=2)
                for pat in patterns:
                    cost = self.computeCost(pat, self.P[k], self.C[k])
                    covered = set()
                    for d, is_on in enumerate(pat):
                        if is_on == 1:
                            covered |= {(j,d) for j in range(self.N) if self.M[i][j] <= self.R[k]}
                    if covered:
                        candidates.append({'i': i, 'k': k, 'pattern': pat, 'cost': cost, 'covered': covered})
        return candidates

    def getBestCandidate(self, candidates, R, used_locations):
        best = None
        best_score = inf
        for cand in candidates:
            if cand['i'] in used_locations:
                continue
            new_cov = cand['covered'] - R
            new_count = len(new_cov)
            if new_count == 0:
                continue
            score = cand['cost'] / new_count  # q(p) = cost / newly_covered
            if score < best_score:
                best_score = score
                best = cand
        return best

    def getRCL(self, candidates, R, used_locations, alpha):
        q_min = inf
        q_max = -inf

        filtered_candidates = [
            c for c in candidates
            if c['i'] not in used_locations and len(c['covered'] - R) > 0
        ]

        for cand in filtered_candidates:
            new_cov = cand['covered'] - R
            new_count = len(new_cov)
            score = cand['cost'] / new_count  # q(p) = cost / newly_covered
            q_min = min(q_min, score)
            q_max = max(q_max, score)

        threshold = q_min + alpha * (q_max - q_min)

        RCL = [
            cand for cand in filtered_candidates
            if (cand['cost'] / len(cand['covered'] - R)) <= threshold
        ]

        return RCL

    def greedySetCover(self, candidates):
        M_univ = set((j, d) for j in range(self.N) for d in range(7))  # universe to cover
        R = set()  # already covered
        chosen = []  # selected candidate objects
        used_locations = set()  # cannot place another camera at same crossing

        cand_list = candidates.copy()

        while R != M_univ:
            best = self.getBestCandidate(cand_list, R, used_locations)

            if best is None:
                # no candidate can add new coverage -> infeasible
                return 'INFEASIBLE'

            # choose best
            chosen.append(best)
            used_locations.add(best['i'])
            R = R.union(best['covered'])

            # remove all candidates at same location (can't place more than one camera per crossing)
            cand_list = [c for c in cand_list if c['i'] != best['i']]

        return chosen
    
    def graspSetCover(self, candidates, alpha=0.3):
        M_univ = set((j, d) for j in range(self.N) for d in range(7))  # universe to cover
        R = set()  # already covered
        chosen = []  # selected candidate objects
        used_locations = set()  # cannot place another camera at same crossing

        cand_list = candidates.copy()

        while R != M_univ:
            RCL = self.getRCL(cand_list, R, used_locations, alpha)
            best = random.choice(RCL) if RCL else None

            if best is None:
                # no candidate can add new coverage -> infeasible
                return 'INFEASIBLE'

            # choose best
            chosen.append(best)
            used_locations.add(best['i'])
            R = R.union(best['covered'])

            # remove all candidates at same location (can't place more than one camera per crossing)
            cand_list = [c for c in cand_list if c['i'] != best['i']]

        return chosen


import time
def main(archivo_datos, alpha=0.3):
    start_time = time.time()
    out = Path('./GRASP') / archivo_datos.name.replace('.dat',f'_{alpha}.grasp.sol')

    K, P, R, A, C, N, M = load_dat_file(archivo_datos) 

    system = CameraSystem(K, P, R, A, C, N, M)

    # print("\nComputing candidates...")
    candidates = system.computeCandidates()
    solution = system.graspSetCover(candidates, alpha=alpha)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


    if solution == 'INFEASIBLE':
        print("\nINFEASIBLE: No valid weekly plan exists.")
        with open(out, "w") as f:
            f.write("INFEASIBLE: No valid weekly plan exists.\n")
            f.write(f"Elapsed time: {elapsed_time:.2f} seconds\n")
    
    else:
        print("\nFeasible GRASP solution found:")
        total_cost = sum(c['cost'] for c in solution)
        with open(out, "w") as f:
            for idx, c in enumerate(solution, 1):

                f.write(f"Camera #{idx}:\n")
                f.write(f"  Crossing: {c['i'] + 1}\n")
                f.write(f"  Model:    {c['k'] + 1}\n")
                f.write(f"  Pattern:  {''.join(str(b) for b in c['pattern'])}\n")
                f.write(f"  Days ON:  {[DAYS[d] for d,b in enumerate(c['pattern']) if b]}\n")
                f.write(f"  Weekly cost: {c['cost']} euros\n\n")

            f.write(f"TOTAL WEEKLY COST = {total_cost} euros\n")
            f.write(f"Elapsed time: {elapsed_time:.2f} seconds\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run GRASP algorithm on camera coverage problem')
    parser.add_argument('datafile', nargs='?', help='Path to .dat file to solve')
    parser.add_argument('-a', '--alpha', type=float, default=0.3, 
                        help='RCL parameter (0=pure greedy, 1=pure random, default=0.3)')

    args = parser.parse_args()

    if args.datafile:
        # Single file mode
        main(Path(args.datafile), alpha=args.alpha)
    else:
        # Batch mode - process all camera_K12*.dat files
        base_dir = Path("../InstanceGeneratorProject/output")
        for archivo_datos in base_dir.glob("camera_K*.dat"):
            main(archivo_datos, alpha=args.alpha)