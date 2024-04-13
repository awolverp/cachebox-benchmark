import cachetools
import pyperf

runner = pyperf.Runner()

# Insert
runner.timeit(
    "insert 100 items",
    "for i in range(100): cache[i] = i",
    "cache = cachetools.Cache(float('inf'))",
    globals=globals()
)

# Delete
def benchmark_delete(loops, cache):
    cache.update({i:i for i in range(loops)})
    range_it = range(loops)

    t0 = pyperf.perf_counter()

    for i in range_it:
        del cache[i]

    return pyperf.perf_counter() - t0

runner.bench_time_func("delete", benchmark_delete, cachetools.Cache(float('inf')))

# Get
runner.timeit(
    "get 100 items",
    "for i in range(100): cache.get(i)",
    "cache = cachetools.Cache(float('inf')); cache.update({i:i for i in range(100)})",
    globals=globals()
)

# update
runner.timeit(
    "update 100 items",
    "cache.update({i:i for i in range(100)})",
    "cache = cachetools.Cache(float('inf'))",
    globals=globals()
)
