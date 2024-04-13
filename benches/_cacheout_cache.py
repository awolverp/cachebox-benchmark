import cacheout
import pyperf

runner = pyperf.Runner()

# Insert
runner.timeit(
    "insert 100 items",
    "for i in range(100): cache.set(i, i)",
    "cache = cacheout.Cache(maxsize=1000000)",
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

runner.bench_time_func("delete", benchmark_delete, cacheout.Cache(maxsize=1000000))

# Get
runner.timeit(
    "get 100 items",
    "for i in range(100): cache.get(i)",
    "cache = cacheout.Cache(maxsize=1000000); cache.add_many({i:i for i in range(100)})",
    globals=globals()
)

# update
runner.timeit(
    "update 100 items",
    "cache.add_many({i:i for i in range(100)})",
    "cache = cacheout.Cache(maxsize=1000000)",
    globals=globals()
)
