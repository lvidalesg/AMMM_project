import numpy as np
import matplotlib.pyplot as plt

# # Data
# instance_size = [8, 40, 84, 154, 285]
# solution_cplex = [82, 452, 214, 159, 262]
# solution_greedy = [87, 495, 219, 180, 326]

# time_cplex=[0.29, 1.02, 0.82, 1.17, 16.37]
# time_greedy=[0.01, 0.03, 0.06, 0.11, 0.23]

# # Compute difference
# diff_solutions = np.array(solution_greedy) - np.array(solution_cplex)
# diff_time = np.array(time_greedy) - np.array(time_cplex)

# # Plot style
# plt.style.use('seaborn-whitegrid')  # nice background and grid

# fig, ax = plt.subplots(figsize=(8,6))

# ax.plot(instance_size, diff_solutions, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=8, label='Difference in Solution (Greedy - CPLEX)')
# ax.plot(instance_size, diff_time, marker='s', linestyle='--', color='#ff7f0e', linewidth=2, markersize=8, label='Difference in Time (Greedy - CPLEX)')
# ax.axhline(0, color='gray', linestyle='--', linewidth=1)  # reference line at 0

# # Labels and title
# ax.set_xlabel('Instance Size (N·K)', fontsize=12, weight='bold')
# ax.set_ylabel('Difference (Greedy - CPLEX)', fontsize=12, weight='bold')
# ax.set_title('Comparison of Solution and Time Quality: CPLEX vs Greedy', fontsize=14, weight='bold')

# # Customize ticks
# ax.tick_params(axis='both', which='major', labelsize=10)

# # Legend
# ax.legend(fontsize=12)

# # Grid
# ax.grid(True, linestyle='--', alpha=0.7)

# # Save figure
# plt.tight_layout()
# plt.savefig('comparison_solution_quality_cplex_greedy.png', dpi=300)
# plt.show()


# New data (generated instances)
new_instance_size = [16,50,84,120,180,216,260,374,432,504]

# greedy results on new instances
new_solution_greedy = [535, 731, 804, 712, 744, 366, 643, 362, 420, 486]
new_time_greedy = [0.01, 0.03, 0.06, 0.09, 0.18, 0.23, 0.32, 0.58, 0.73, 0.92]

# cplex results on new instances
new_solution_cplex = [464, 643, 596, 562, 537, 352, 514, 332, 400]
new_time_cplex = [0.16, 0.78, 1.35, 1.36, 5.47, 35.91, 1109.93, 1501.12, 1800] # el ultimo es 5180.15 segundos 

# Compute difference for new instances
new_diff_solutions = np.array(new_solution_greedy[:len(new_solution_cplex)]) - np.array(new_solution_cplex)
new_diff_time = np.array(new_time_greedy[:len(new_time_cplex)]) - np.array(new_time_cplex)

# Plot for new instances
fig, ax = plt.subplots(figsize=(8,6))
ax.plot(new_instance_size[:len(new_diff_solutions)], new_diff_solutions, marker='o', linestyle='-', color='#2ca02c', linewidth=2, markersize=8, label='Difference in Solution (Greedy - CPLEX)')
ax.plot(new_instance_size[:len(new_diff_time)], new_diff_time, marker='s', linestyle='-', color='#d62728', linewidth=2, markersize=8, label='Difference in Time (Greedy - CPLEX)')
ax.axhline(0, color='gray', linestyle='-', linewidth=1)    

ax.set_xlabel('Instance Size (N·K)', fontsize=12, weight='bold')
ax.set_ylabel('Difference (Greedy - CPLEX)', fontsize=12, weight='bold')
ax.set_title('Comparison of Solution and Time Quality: CPLEX vs Greedy', fontsize=14, weight='bold')

ax.tick_params(axis='both', which='major', labelsize=10)    

ax.legend(fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('comparison_solution_quality_cplex_greedy_generated_instances.png', dpi=300)
plt.show()
