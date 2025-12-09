import numpy as np
import matplotlib.pyplot as plt

instance_size = [16,50,84,120,180,216,260,374,432]#,504]

# greedy results on new instances
solution_greedy = [535, 731, 804, 712, 744, 366, 643, 362, 420]#, 486]
time_greedy = [0.05063733, 0.06133484, 0.10973359, 0.08632803, 0.13650274, 0.18301274, 0.20850492, 0.39717421, 0.46352476, 0.65117704]

# cplex results on new instances
solution_cplex = [464, 643, 596, 562, 537, 352, 514, 332, 400]
time_cplex = [0.16, 0.78, 1.35, 1.36, 5.47, 35.91, 1109.93, 1501.12, 1800] # el ultimo es 5180.15 segundos pero se pasa de los 30 min=1800s

solution_greedy_ls = [472, 697, 804, 712, 744, 366, 643, 362, 420, 486]
time_greedy_ls = [
    0.051645202,
    0.063367335,
    0.07590581,
    0.091282831,
    0.144966776,
    0.193925928,
    0.200028291,
    0.394574747,
    0.46809043,
    0.64568755
]

solution_grasp_03 = [
    1119,  # camera_K2_N8_0
    None,  # camera_K5_N10_0 (INFEASIBLE)
    None,  # camera_K6_N14_0 (INFEASIBLE)
    None,  # camera_K8_N15_0 (INFEASIBLE)
    1825,  # camera_K9_N20_0
    1808,  # camera_K9_N24_0
    2405,  # camera_K10_N26_0
    2788,  # camera_K11_N34_0
    2218,  # camera_K12_N36_0
    2629   # camera_K14_N36_0
]
time_grasp_03 = [
    0.01,  # camera_K2_N8_0
    0.03,  # camera_K5_N10_0
    0.06,  # camera_K6_N14_0
    0.09,  # camera_K8_N15_0
    0.17,  # camera_K9_N20_0
    0.44,  # camera_K9_N24_0
    0.39,  # camera_K10_N26_0
    1.34,  # camera_K11_N34_0
    1.21,  # camera_K12_N36_0
    1.78   # camera_K14_N36_0
]

solution_grasp_05 = [
    1190,  # camera_K2_N8_0
    None,  # camera_K5_N10_0 (INFEASIBLE)
    1651,  # camera_K6_N14_0
    None,  # camera_K8_N15_0 (INFEASIBLE)
    2050,  # camera_K9_N20_0
    1815,  # camera_K9_N24_0
    2334,  # camera_K10_N26_0
    2444,  # camera_K11_N34_0
    2693,  # camera_K12_N36_0
    2771   # camera_K14_N36_0
]
time_grasp_05 = [
    0.01,  # camera_K2_N8_0
    0.02,  # camera_K5_N10_0
    0.04,  # camera_K6_N14_0
    0.07,  # camera_K8_N15_0
    0.17,  # camera_K9_N20_0
    0.30,  # camera_K9_N24_0
    0.30,  # camera_K10_N26_0
    1.03,  # camera_K11_N34_0
    0.87,  # camera_K12_N36_0
    1.56   # camera_K14_N36_0
]

solution_grasp_07 = [
    None,  # camera_K2_N8_0 (INFEASIBLE)
    None,  # camera_K5_N10_0 (INFEASIBLE)
    None,  # camera_K6_N14_0 (INFEASIBLE)
    None,  # camera_K8_N15_0 (INFEASIBLE)
    None,  # camera_K9_N20_0 (INFEASIBLE)
    2463,  # camera_K9_N24_0
    2663,  # camera_K10_N26_0
    3396,  # camera_K11_N34_0
    2989,  # camera_K12_N36_0
    2596   # camera_K14_N36_0
]
time_grasp_07 = [
    0.01,  # camera_K2_N8_0
    0.02,  # camera_K5_N10_0
    0.04,  # camera_K6_N14_0
    0.07,  # camera_K8_N15_0
    0.18,  # camera_K9_N20_0
    0.36,  # camera_K9_N24_0
    0.35,  # camera_K10_N26_0
    1.36,  # camera_K11_N34_0
    1.20,  # camera_K12_N36_0
    1.62   # camera_K14_N36_0
]

# Compute metrics relative to CPLEX
n = len(solution_cplex)
solution_cplex_arr = np.array(solution_cplex)
time_cplex_arr = np.array(time_cplex[:n])

# Solution quality difference (Heuristic - CPLEX)
diff_greedy = np.array(solution_greedy[:n]) - solution_cplex_arr
diff_greedy_ls = np.array(solution_greedy_ls[:n]) - solution_cplex_arr

# Time speedup (relative to CPLEX, i.e., CPLEX_time / Heuristic_time)
speedup_greedy = time_cplex_arr / np.array(time_greedy[:n])
speedup_greedy_ls = time_cplex_arr / np.array(time_greedy_ls[:n])

# Create two separate plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Solution Quality (difference from CPLEX optimal)
ax1.plot(instance_size[:n], diff_greedy, marker='o', linestyle='-', color='#2ca02c', 
         linewidth=2, markersize=8, label='Greedy')
ax1.plot(instance_size[:n], diff_greedy_ls, marker='s', linestyle='-', color='#ff7f0e', 
         linewidth=2, markersize=8, label='Greedy + Local Search')
ax1.axhline(0, color='gray', linestyle='--', linewidth=1.5, label='CPLEX Optimal')
ax1.set_xlabel('Instance Size (N·K)', fontsize=12, weight='bold')
ax1.set_ylabel('Solution Quality Gap (euros)', fontsize=12, weight='bold')
ax1.set_title('Solution Quality vs CPLEX\n(Lower is Better)', fontsize=14, weight='bold')
ax1.tick_params(axis='both', which='major', labelsize=10)
ax1.legend(fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.7)

# Plot 2: Execution Time Speedup (relative to CPLEX)
ax2.plot(instance_size[:n], speedup_greedy, marker='o', linestyle='-', color='#2ca02c', 
         linewidth=2, markersize=8, label='Greedy')
ax2.plot(instance_size[:n], speedup_greedy_ls, marker='s', linestyle='-', color='#ff7f0e', 
         linewidth=2, markersize=8, label='Greedy + Local Search')
ax2.axhline(1, color='gray', linestyle='--', linewidth=1.5, label='CPLEX Baseline (1x)')
ax2.set_xlabel('Instance Size (N·K)', fontsize=12, weight='bold')
ax2.set_ylabel('Speedup (×)', fontsize=12, weight='bold')
ax2.set_title('Execution Time Speedup vs CPLEX\n(Higher is Better)', fontsize=14, weight='bold')
ax2.tick_params(axis='both', which='major', labelsize=10)
ax2.legend(fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.set_yscale('log')

plt.tight_layout()
plt.savefig('comparison_cplex_vs_heuristics.png', dpi=300)
plt.show()

# ===== GRASP with different alpha values =====
# Convert lists to arrays, handling None values
def to_array_with_nan(lst, length):
    """Convert list to numpy array, replacing None with NaN"""
    arr = []
    for i in range(length):
        if i < len(lst) and lst[i] is not None:
            arr.append(lst[i])
        else:
            arr.append(np.nan)
    return np.array(arr)

# Prepare GRASP data
grasp_03_sol = to_array_with_nan(solution_grasp_03, n)
grasp_05_sol = to_array_with_nan(solution_grasp_05, n)
grasp_07_sol = to_array_with_nan(solution_grasp_07, n)

grasp_03_time = np.array(time_grasp_03[:n])
grasp_05_time = np.array(time_grasp_05[:n])
grasp_07_time = np.array(time_grasp_07[:n])

# Compute differences and speedups for GRASP
diff_grasp_03 = grasp_03_sol - solution_cplex_arr
diff_grasp_05 = grasp_05_sol - solution_cplex_arr
diff_grasp_07 = grasp_07_sol - solution_cplex_arr

speedup_grasp_03 = time_cplex_arr / grasp_03_time
speedup_grasp_05 = time_cplex_arr / grasp_05_time
speedup_grasp_07 = time_cplex_arr / grasp_07_time

# Create plots for GRASP comparison
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 3: GRASP Solution Quality with different alphas
ax3.plot(instance_size[:n], diff_grasp_03, marker='o', linestyle='-', color='#1f77b4', 
         linewidth=2, markersize=8, label=r'GRASP ($\alpha=0.3$)')
ax3.plot(instance_size[:n], diff_grasp_05, marker='s', linestyle='-', color='#ff7f0e', 
         linewidth=2, markersize=8, label=r'GRASP ($\alpha=0.5$)')
ax3.plot(instance_size[:n], diff_grasp_07, marker='^', linestyle='-', color='#2ca02c', 
         linewidth=2, markersize=8, label=r'GRASP ($\alpha=0.7$)')
ax3.axhline(0, color='gray', linestyle='--', linewidth=1.5, label='CPLEX Optimal')
ax3.set_xlabel('Instance Size (N·K)', fontsize=12, weight='bold')
ax3.set_ylabel('Solution Quality Gap (euros)', fontsize=12, weight='bold')
ax3.set_title('GRASP Solution Quality vs CPLEX\n(Lower is Better)', fontsize=14, weight='bold')
ax3.tick_params(axis='both', which='major', labelsize=10)
ax3.legend(fontsize=11)
ax3.grid(True, linestyle='--', alpha=0.7)

# Plot 4: GRASP Execution Time Speedup
ax4.plot(instance_size[:n], speedup_grasp_03, marker='o', linestyle='-', color='#1f77b4', 
         linewidth=2, markersize=8, label=r'GRASP ($\alpha=0.3$)')
ax4.plot(instance_size[:n], speedup_grasp_05, marker='s', linestyle='-', color='#ff7f0e', 
         linewidth=2, markersize=8, label=r'GRASP ($\alpha=0.5$)')
ax4.plot(instance_size[:n], speedup_grasp_07, marker='^', linestyle='-', color='#2ca02c', 
         linewidth=2, markersize=8, label=r'GRASP ($\alpha=0.7$)')
ax4.axhline(1, color='gray', linestyle='--', linewidth=1.5, label='CPLEX Baseline (1x)')
ax4.set_xlabel('Instance Size (N·K)', fontsize=12, weight='bold')
ax4.set_ylabel('Speedup (×)', fontsize=12, weight='bold')
ax4.set_title('GRASP Execution Time Speedup vs CPLEX\n(Higher is Better)', fontsize=14, weight='bold')
ax4.tick_params(axis='both', which='major', labelsize=10)
ax4.legend(fontsize=11)
ax4.grid(True, linestyle='--', alpha=0.7)
ax4.set_yscale('log')

plt.tight_layout()
plt.savefig('comparison_cplex_vs_grasp_alphas.png', dpi=300)
plt.show()
