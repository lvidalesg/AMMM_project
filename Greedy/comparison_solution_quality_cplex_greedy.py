import numpy as np
import matplotlib.pyplot as plt

new_instance_size = [16,50,84,120,180,216,260,374,432,504]

# greedy results on new instances
solution_greedy = [535, 731, 804, 712, 744, 366, 643, 362, 420, 486]
time_greedy = [0.01, 0.03, 0.06, 0.09, 0.18, 0.23, 0.32, 0.58, 0.73, 0.92]

# cplex results on new instances
solution_cplex = [464, 643, 596, 562, 537, 352, 514, 332, 400]
time_cplex = [0.16, 0.78, 1.35, 1.36, 5.47, 35.91, 1109.93, 1501.12, 1800] # el ultimo es 5180.15 segundos 

# Compute difference for new instances
diff_solutions = np.array(solution_greedy[:len(solution_cplex)]) - np.array(solution_cplex)
diff_time = np.array(time_greedy[:len(time_cplex)]) - np.array(time_cplex)

# Plot for new instances
fig, ax = plt.subplots(figsize=(8,6))
ax.plot(new_instance_size[:len(diff_solutions)], diff_solutions, marker='o', linestyle='-', color='#2ca02c', linewidth=2, markersize=8, label='Difference in Solution (Greedy - CPLEX)')
ax.plot(new_instance_size[:len(diff_time)], diff_time, marker='s', linestyle='-', color='#d62728', linewidth=2, markersize=8, label='Difference in Time (Greedy - CPLEX)')
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
