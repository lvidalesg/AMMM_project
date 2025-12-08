from itertools import product
from load_data_python import load_dat_file
from math import inf


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

    def is_pattern_valid(self, pattern, A_k):
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

    def all_valid_patterns(self, A_k):
        """Return list of patterns (tuples) valid for autonomy A_k."""
        patterns = []
        for bits in product([0,1], repeat=7):
            if self.is_pattern_valid(bits, A_k):
                patterns.append(bits)
        return patterns


    def compute_coverages(self):
        """
        Returns list of candidate plans:
        each candidate is dict with keys:
        - 'i': location (0-based)
        - 'k': model (0-based)
        - 'pattern': tuple of 7 bits
        - 'days_on': int
        - 'cost': P_k + days_on * C_k
        - 'covered': set of (node, day) pairs (0-based)
        """
        candidates = []
        for i in range(self.N):
            for k in range(self.K):
                patterns = self.all_valid_patterns(self.A[k])
                # If no valid pattern exists for this A[k], continue (shouldn't happen with A>=2)
                for pat in patterns:
                    days_on = sum(pat)
                    cost = self.P[k] + days_on * self.C[k]
                    covered = set()
                    for d, bit in enumerate(pat):
                        if bit == 1:
                            # for all nodes j that spatially are covered by camera (i,k)
                            for j in range(self.N):
                                if self.M[i][j] <= self.R[k]:
                                    covered.add((j, d))
                    if covered:
                        candidates.append({'i': i, 'k': k, 'pattern': pat, 'days_on': days_on, 'cost': cost, 'covered': covered})
        return candidates


    def greedy_set_cover(self, candidates):
        M = set((j, d) for j in range(self.N) for d in range(7))  # universe to cover
        R = set()  # already covered
        chosen = []  # selected candidate objects
        used_locations = set()  # cannot place another camera at same crossing

        # Pre-filter candidates: we will maintain dynamic list
        cand_list = candidates.copy()

        while R != M:
            best = None
            best_score = inf

            for cand in cand_list:
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



import glob

def main():
    for archivo_datos in glob.glob("project.*.dat"):
        K, P, R, A, C, N, M = load_dat_file(archivo_datos) 

        system = CameraSystem(K, P, R, A, C, N, M)

        # print("\nComputing candidates...")
        candidates = system.compute_coverages()
        # print(f"Total candidates: {len(candidates)}")

        # print("\nRunning greedy set cover...")
        solution = system.greedy_set_cover(candidates)

        if solution == 'INFEASIBLE':
            print("\nINFEASIBLE: No valid weekly plan exists.")
            with open('Greedy\\' + archivo_datos.replace('.dat','.greedy.sol'), "w") as f:
                f.write("INFEASIBLE: No valid weekly plan exists.\n")
        
        else:
            print("\nFeasible greedy solution found:")
            total_cost = sum(c['cost'] for c in solution)
            with open('Greedy\\' + archivo_datos.replace('.dat','.greedy.sol'), "w") as f:
                for idx, c in enumerate(solution, 1):
                    # print(f"\nCamera #{idx}:")
                    # print(f"  Crossing: {c['i'] + 1}")
                    # print(f"  Model:    {c['k'] + 1}")
                    # print(f"  Pattern:  {''.join(str(b) for b in c['pattern'])}")
                    # print(f"  Days ON:  {[DAYS[d] for d,b in enumerate(c['pattern']) if b]}")
                    # print(f"  Weekly cost: {c['cost']} euros")

                    # Escribir lo mismo en el archivo .sol
                    f.write(f"Camera #{idx}:\n")
                    f.write(f"  Crossing: {c['i'] + 1}\n")
                    f.write(f"  Model:    {c['k'] + 1}\n")
                    f.write(f"  Pattern:  {''.join(str(b) for b in c['pattern'])}\n")
                    f.write(f"  Days ON:  {[DAYS[d] for d,b in enumerate(c['pattern']) if b]}\n")
                    f.write(f"  Weekly cost: {c['cost']} euros\n\n")

                # print(f"\nTOTAL WEEKLY COST = {total_cost} euros")
                f.write(f"TOTAL WEEKLY COST = {total_cost} euros\n")



if __name__ == "__main__":
    main()