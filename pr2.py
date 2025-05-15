import pandas as pd
from functools import lru_cache

# Кешована функція
@lru_cache(maxsize=None)
def cached_add(a, b):
    return a + b  # або інша обробка

# Створення DataFrame
df = pd.DataFrame({
    'a': [1, 2, 2, 3],
    'b': [4, 5, 5, 6]
})

# Використання кешованої функції всередині apply
result = df.apply(lambda row: cached_add(row['a'], row['b']), axis=1)

print(result)







