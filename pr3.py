import random
from datetime import datetime, timedelta
from collections import defaultdict
import time

# Генерація фейкових даних
def generate_data(num_records=100_000):
    groups = ['residential', 'commercial', 'industrial']
    base_time = datetime(2020, 1, 1)
    data = []

    for _ in range(num_records):
        entry = {
            'consumer_id': random.randint(1, 1000),
            'group': random.choice(groups),
            'timestamp': base_time + timedelta(minutes=random.randint(0, 1_500_000)),
            'energy_kWh': round(random.uniform(0.1, 10.0), 2)
        }
        data.append(entry)
    return data

# Агрегація на заданому рівні
def aggregate(data, level='day'):
    agg = defaultdict(float)

    for entry in data:
        ts = entry['timestamp']
        group = entry['group']
        if level == 'day':
            key = (group, ts.year, ts.month, ts.day)
        elif level == 'month':
            key = (group, ts.year, ts.month)
        elif level == 'year':
            key = (group, ts.year)
        else:
            raise ValueError("Unsupported level: choose 'day', 'month', or 'year'")

        agg[key] += entry['energy_kWh']

    return agg

# Основна функція
def main():
    print("Генерація даних...")
    data = generate_data()

    for level in ['day', 'month', 'year']:
        start = time.time()
        result = aggregate(data, level)
        end = time.time()
        print(f"Агрегація за {level:5} - Кількість записів: {len(result):6} | Час виконання: {end - start:.4f} секунд")

        # Приклад кількох результатів
        for i, (k, v) in enumerate(result.items()):
            print(f"  {k} -> {v:.2f} кВт⋅год")
            if i >= 2:
                break
        print()

if __name__ == "__main__":
    main()
