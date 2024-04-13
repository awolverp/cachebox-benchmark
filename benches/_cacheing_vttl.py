import cacheing
import pyperf
import random

runner = pyperf.Runner()

# Insert
runner.timeit(
    "insert 1000 items",
    "for i in range(1000): cache[i, random.randint(1, 10)] = i",
    "cache = cacheing.VTTLCache(100)",
    globals=globals()
)

# Get
runner.timeit(
    "get 100 items",
    "for i in range(100): cache.get(i)",
    "cache = cacheing.VTTLCache(100); cache.update({(i, 2):i for i in range(100)})",
    globals=globals()
)

# update
runner.timeit(
    "update 1000 items",
    "cache.update({(i, 2):i for i in range(1000)})",
    "cache = cacheing.VTTLCache(100)",
    globals=globals()
)
