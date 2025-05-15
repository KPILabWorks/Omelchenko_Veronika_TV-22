import numpy as np
import matplotlib.pyplot as plt

# Параметри симуляції
num_sensors = 100
num_nodes = 5
simulation_steps = 60

# Ємність вузлів (байт/сек)
node_capacity = np.array([1000] * num_nodes)

# Латентність між сенсорами та вузлами
np.random.seed(42)
latency_matrix = np.random.randint(50, 200, size=(num_sensors, num_nodes))

# Швидкість передачі даних сенсорів
sensor_data_rates = np.random.randint(10, 50, size=num_sensors)

# Статична стратегія (round-robin)
def static_strategy(sensor_id):
    return sensor_id % num_nodes

# Динамічна стратегія (на основі навантаження та латентності)
def dynamic_strategy(sensor_id, node_loads):
    best_score = float('inf')
    best_node = None
    for j in range(num_nodes):
        projected_load = node_loads[j] + sensor_data_rates[sensor_id]
        if projected_load <= node_capacity[j]:
            score = latency_matrix[sensor_id, j] + projected_load / node_capacity[j]
            if score < best_score:
                best_score = score
                best_node = j
    return best_node

# Симуляція
def simulate(strategy_func, name):
    node_loads = np.zeros(num_nodes)
    total_latency = 0
    overloaded = 0
    load_distribution = []

    for t in range(simulation_steps):
        node_loads[:] = 0
        for i in range(num_sensors):
            if strategy_func == static_strategy:
                node = strategy_func(i)
            else:
                node = strategy_func(i, node_loads)
            if node is not None:
                projected_load = node_loads[node] + sensor_data_rates[i]
                if projected_load <= node_capacity[node]:
                    node_loads[node] += sensor_data_rates[i]
                    total_latency += latency_matrix[i, node]
                else:
                    overloaded += 1
            else:
                overloaded += 1
        load_distribution.append(node_loads.copy())

    avg_latency = total_latency / (simulation_steps * num_sensors - overloaded)
    return {
        'strategy': name,
        'avg_latency': avg_latency,
        'lost_packets': overloaded,
        'load_distribution': np.array(load_distribution)
    }

# Запуск симуляцій
results = []
results.append(simulate(static_strategy, 'Статична'))
results.append(simulate(dynamic_strategy, 'Інтелектуальна'))

# Побудова графіку
labels = [res['strategy'] for res in results]
latencies = [res['avg_latency'] for res in results]
losses = [res['lost_packets'] for res in results]

x = np.arange(len(labels))
width = 0.35

fig, ax1 = plt.subplots(figsize=(10, 6))

# Графік середньої затримки
bar1 = ax1.bar(x - width/2, latencies, width, label='Середня затримка (мс)', color='steelblue')
ax1.set_ylabel('Середня затримка (мс)')
ax1.set_title('Порівняння стратегій балансування навантаження в IoT-мережах')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)

# Графік втрат пакетів
ax2 = ax1.twinx()
bar2 = ax2.bar(x + width/2, losses, width, label='Втрати даних', color='indianred')
ax2.set_ylabel('Кількість втрачених пакетів')

# Легенда
fig.legend(loc='upper right', bbox_to_anchor=(0.85, 0.85))
plt.tight_layout()
plt.show()








