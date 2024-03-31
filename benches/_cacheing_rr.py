import cacheing
import pyperf

runner = pyperf.Runner()

# Insert
runner.timeit(
    "insert 1000 items",
    "for i in range(1000): cache[i] = i",
    "cache = cacheing.RandomCache(100)",
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

runner.bench_time_func("delete", benchmark_delete, cacheing.RandomCache(float('inf')))

# Clear
def benchmark_clear(loops, cache):
    cache.update({i:i for i in range(loops)})

    t0 = pyperf.perf_counter()
    cache.clear()
    return pyperf.perf_counter() - t0

runner.bench_time_func("clear", benchmark_clear, cacheing.RandomCache(float('inf')))

# Get
runner.timeit(
    "get 100 items",
    "for i in range(100): cache.get(i)",
    "cache = cacheing.RandomCache(100); cache.update({i:i for i in range(100)})",
    globals=globals()
)

# update
runner.timeit(
    "update 1000 items",
    "cache.update({i:i for i in range(1000)})",
    "cache = cacheing.RandomCache(100)",
    globals=globals()
)
