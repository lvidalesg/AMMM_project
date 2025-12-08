from itertools import product
from load_data_python import load_dat_file
from math import inf
import glob
import random
import copy

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


    def greedy_randomized_construction(self, candidates, alpha=0.3):
        """
        GRASP construction phase: build a solution using semi-greedy randomized approach.
        alpha: controls randomization (0 = pure greedy, 1 = pure random)
        """
        M_univ = set((j, d) for j in range(self.N) for d in range(7))  # universe to cover
        R = set()  # already covered
        chosen = []  # selected candidate objects
        used_locations = set()  # cannot place another camera at same crossing

        cand_list = candidates.copy()

        while R != M_univ:
            # Calculate scores for all valid candidates
            valid_candidates = []
            for cand in cand_list:
                if cand['i'] in used_locations:
                    continue
                new_cov = cand['covered'] - R
                new_count = len(new_cov)
                if new_count == 0:
                    continue
                score = cand['cost'] / new_count  # q(p) = cost / newly_covered
                valid_candidates.append((cand, score))

            if not valid_candidates:
                # no candidate can add new coverage -> infeasible
                return 'INFEASIBLE'

            # Find min and max scores
            scores = [score for _, score in valid_candidates]
            min_score = min(scores)
            max_score = max(scores)

            # Build Restricted Candidate List (RCL)
            # RCL contains candidates with score <= min_score + alpha * (max_score - min_score)
            threshold = min_score + alpha * (max_score - min_score)
            rcl = [cand for cand, score in valid_candidates if score <= threshold]

            # Randomly select from RCL
            best = random.choice(rcl)

            # Add selected candidate to solution
            chosen.append(best)
            used_locations.add(best['i'])
            R = R.union(best['covered'])

            # remove all candidates at same location (can't place more than one camera per crossing)
            cand_list = [c for c in cand_list if c['i'] != best['i']]

        return chosen


    def local_search(self, solution, candidates):
        """
        Local search phase: try to improve solution by swapping cameras.
        Returns improved solution or original if no improvement found.
        """
        if solution == 'INFEASIBLE':
            return solution

        improved = True
        current_solution = copy.deepcopy(solution)
        current_cost = sum(c['cost'] for c in current_solution)

        while improved:
            improved = False
            
            # Try removing one camera and replacing with another
            for idx, camera in enumerate(current_solution):
                # Try removing this camera
                temp_solution = current_solution[:idx] + current_solution[idx+1:]
                used_locations = {c['i'] for c in temp_solution}
                covered = set()
                for c in temp_solution:
                    covered = covered.union(c['covered'])
                
                # What needs to be covered?
                M_univ = set((j, d) for j in range(self.N) for d in range(7))
                missing = M_univ - covered
                
                if not missing:
                    # Solution still valid without this camera
                    new_cost = sum(c['cost'] for c in temp_solution)
                    if new_cost < current_cost:
                        current_solution = temp_solution
                        current_cost = new_cost
                        improved = True
                        break
                else:
                    # Try to find a better replacement camera
                    for new_cand in candidates:
                        if new_cand['i'] in used_locations or new_cand['i'] == camera['i']:
                            continue
                        
                        # Check if new candidate + remaining cameras cover everything
                        test_solution = temp_solution + [new_cand]
                        test_covered = covered.union(new_cand['covered'])
                        
                        if test_covered == M_univ:
                            new_cost = sum(c['cost'] for c in test_solution)
                            if new_cost < current_cost:
                                current_solution = test_solution
                                current_cost = new_cost
                                improved = True
                                break
                
                if improved:
                    break

        return current_solution


    def grasp(self, candidates, max_iterations=100, alpha=0.3):
        """
        GRASP metaheuristic: iterate construction + local search
        Returns best solution found.
        """
        best_solution = None
        best_cost = inf

        for iteration in range(max_iterations):
            # Construction phase
            solution = self.greedy_randomized_construction(candidates, alpha)
            
            if solution == 'INFEASIBLE':
                continue

            # Local search phase
            solution = self.local_search(solution, candidates)

            # Update best solution
            cost = sum(c['cost'] for c in solution)
            if cost < best_cost:
                best_cost = cost
                best_solution = copy.deepcopy(solution)
                print(f"Iteration {iteration + 1}: New best cost = {best_cost}")

        return best_solution if best_solution is not None else 'INFEASIBLE'


    def greedy_set_cover(self, candidates):
        """
        Pure greedy set cover (for comparison).
        """
        M_univ = set((j, d) for j in range(self.N) for d in range(7))  # universe to cover
        R = set()  # already covered
        chosen = []  # selected candidate objects
        used_locations = set()  # cannot place another camera at same crossing

        cand_list = candidates.copy()

        while R != M_univ:
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



import time
import os

def main(archivo_datos, max_iterations=100, alpha=0.3, use_grasp=True):
    """
    Main function to solve camera coverage problem.
    
    Parameters:
    - archivo_datos: path to .dat file
    - max_iterations: number of GRASP iterations (default: 100)
    - alpha: randomization parameter for RCL (0=pure greedy, 1=pure random, default: 0.3)
    - use_grasp: if True, use GRASP; if False, use pure greedy (default: True)
    """
    start_time = time.time()

    K, P, R, A, C, N, M = load_dat_file(archivo_datos) 

    system = CameraSystem(K, P, R, A, C, N, M)

    print(f"\nComputing candidates for {os.path.basename(archivo_datos)}...")
    candidates = system.compute_coverages()
    print(f"Total candidates: {len(candidates)}")

    # Choose algorithm
    if use_grasp:
        print(f"\nRunning GRASP (iterations={max_iterations}, alpha={alpha})...")
        solution = system.grasp(candidates, max_iterations=max_iterations, alpha=alpha)
    else:
        print("\nRunning pure greedy algorithm...")
        solution = system.greedy_set_cover(candidates)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    # Prepare output filename
    output_dir = os.path.join(os.path.dirname(os.path.dirname(archivo_datos)), "GRASP")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(archivo_datos).replace('.dat', '.grasp.sol'))

    if solution == 'INFEASIBLE':
        print("\nINFEASIBLE: No valid weekly plan exists.")
        with open(output_file, "w") as f:
            f.write("INFEASIBLE: No valid weekly plan exists.\n")
            f.write(f"Elapsed time: {elapsed_time:.2f} seconds\n")
    
    else:
        print("\nFeasible solution found:")
        total_cost = sum(c['cost'] for c in solution)
        print(f"TOTAL WEEKLY COST = {total_cost} euros")
        
        with open(output_file, "w") as f:
            f.write(f"{'GRASP' if use_grasp else 'Greedy'} Solution\n")
            if use_grasp:
                f.write(f"Parameters: max_iterations={max_iterations}, alpha={alpha}\n")
            f.write("="*50 + "\n\n")
            
            for idx, c in enumerate(solution, 1):
                f.write(f"Camera #{idx}:\n")
                f.write(f"  Crossing: {c['i'] + 1}\n")
                f.write(f"  Model:    {c['k'] + 1}\n")
                f.write(f"  Pattern:  {''.join(str(b) for b in c['pattern'])}\n")
                f.write(f"  Days ON:  {[DAYS[d] for d,b in enumerate(c['pattern']) if b]}\n")
                f.write(f"  Weekly cost: {c['cost']} euros\n\n")

            f.write(f"\nTOTAL WEEKLY COST = {total_cost} euros\n")
            f.write(f"Elapsed time: {elapsed_time:.2f} seconds\n")
        
        print(f"Solution saved to: {output_file}")


if __name__ == "__main__":
    import sys
    
    current_dir = os.getcwd()
    print("Current directory:", current_dir)

    # Parse command line arguments
    if len(sys.argv) > 1:
        # Single file mode
        data_file = sys.argv[1]
        max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        alpha_val = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
        use_grasp = sys.argv[4].lower() != 'false' if len(sys.argv) > 4 else True
        
        main(data_file, max_iterations=max_iter, alpha=alpha_val, use_grasp=use_grasp)
    else:
        # Batch mode - process all instance files
        data_pattern = os.path.join(current_dir, "InstanceGeneratorProject", "output", "**", "*.dat")
        import glob
        
        files = glob.glob(data_pattern, recursive=True)
        if not files:
            print("No .dat files found in InstanceGeneratorProject/output/")
            print("Usage: python grasp.py <datafile.dat> [max_iterations] [alpha] [use_grasp]")
        else:
            print(f"Found {len(files)} instance files to process\n")
            for archivo_datos in files[:5]:  # Process first 5 files as example
                main(archivo_datos, max_iterations=50, alpha=0.3, use_grasp=True)
                print("\n" + "="*80 + "\n")