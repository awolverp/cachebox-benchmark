import cacheout
import pyperf

runner = pyperf.Runner()

# Insert
runner.timeit(
    "insert 1000 items",
    "for i in range(1000): cache.set(i, i)",
    "cache = cacheout.FIFOCache(maxsize=100)",
    globals=globals()
)

# Delete
def benchmark_delete(loops, cache):
    cache.add_many({i:i for i in range(loops)})
    range_it = range(loops)

    t0 = pyperf.perf_counter()

    for i in range_it:
        cache.delete(i)

    return pyperf.perf_counter() - t0

runner.bench_time_func("delete", benchmark_delete, cacheout.FIFOCache(maxsize=100000))

# Get
runner.timeit(
    "get 100 items",
    "for i in range(100): cache.get(i)",
    "cache = cacheout.FIFOCache(maxsize=100); cache.add_many({i:i for i in range(100)})",
    globals=globals()
)

# update
runner.timeit(
    "update 1000 items",
    "cache.add_many({i:i for i in range(1000)})",
    "cache = cacheout.FIFOCache(maxsize=100)",
    globals=globals()
)
