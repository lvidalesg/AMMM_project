import matplotlib.pyplot as plt

# Datos
N_values = [2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40]
k2_times = [0.3250, 0.1690, 0.1780, 1.1600, 1.4740, 25.9160, 162.7480, 102.0920, 175.7400, 1345.3930]#, 471.8190]

# Estilo del gráfico
plt.style.use('default')
fig, ax = plt.subplots(figsize=(10,6))


ax.plot(N_values[:len(k2_times)], k2_times, marker='o', linestyle='-', color='#ff7f0e', linewidth=2, markersize=8, label='K=2')

# Configuración de ejes
ax.set_xlabel('Number of Crossings (N)', fontsize=12, weight='bold')
ax.set_ylabel('CPLEX Time (seconds, log scale)', fontsize=12, weight='bold')
ax.set_title('CPLEX Time vs Number of Crossings for K=2', fontsize=14, weight='bold')
ax.set_yscale('log')

ax.legend(fontsize=12)

ax.tick_params(axis='both', which='major', labelsize=10)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('cplex_time_vs_N_K2.png', dpi=300)
plt.show()


#  k=4
N_values = [2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40]
k4_times = [0.28, 0.1, 0.27, 1.03, 3.80, 40.16, 10.53, 124.17, 621.74, 1800]

plt.style.use('default')
fig, ax = plt.subplots(figsize=(10,6))


ax.plot(N_values[:len(k2_times)], k2_times, marker='o', linestyle='-', color='#ff7f0e', linewidth=2, markersize=8, label='K=2')
ax.plot(N_values[:len(k4_times)], k4_times, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=8, label='K=4')

ax.set_xlabel('Number of Crossings (N)', fontsize=12, weight='bold')
ax.set_ylabel('CPLEX Time (seconds, log scale)', fontsize=12, weight='bold')
ax.set_title('CPLEX Time vs Number of Crossings for K=2,4', fontsize=14, weight='bold')
ax.set_yscale('log')

ax.legend(fontsize=12)

ax.tick_params(axis='both', which='major', labelsize=10)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('cplex_time_vs_N_K2_4.png', dpi=300)
plt.show()