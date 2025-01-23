from measure import GroupBenchmark, Benchmark, PerfCtx
import random
import os.path
import sys
import os

import cachetools
import cachebox
import cacheing
import lru

if not os.path.exists("plots"):
    os.mkdir("plots")


class EqVal:
    def __init__(self, n: int) -> None:
        self.val = n

    def __eq__(self, value: "EqVal") -> bool:
        return self.val == value.val

    def __hash__(self) -> int:
        return hash(self.val)


class _bench_protocol:
    def __init__(
        self, cache: cachebox.BaseCacheImpl, way: str = "setitem", use_eq: bool = False
    ) -> None:
        self.cache = cache
        self.way = way
        self.use_eq = use_eq

    def __call__(self, ctx: PerfCtx, n: int):
        if self.use_eq:
            n = EqVal(n)

        if self.way == "setitem":
            with ctx:
                self.cache[n] = n
                self.cache[n]

        elif self.way == "vttl_insert":
            rnd = random.randint(1, 10)

            with ctx:
                self.cache.insert(n, n, rnd)
                self.cache[n]

        elif self.way == "vttl_setitem":
            rnd = random.randint(1, 10)

            with ctx:
                self.cache[(n, rnd)] = n
                self.cache[n]

        else:
            raise ValueError("invalid way")


benches_dict = {
    "cache": GroupBenchmark(
        "Cache (include dictionary)",
        Benchmark("dict()", _bench_protocol(dict()), range_n=100000, repeat=200),
        Benchmark(
            "cachebox.Cache(100000)",
            _bench_protocol(cachebox.Cache(100000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.Cache(100000)",
            _bench_protocol(cachetools.Cache(100000)),
            range_n=100000,
            repeat=300,
        ),
    ),
    "cache_eq": GroupBenchmark(
        "Cache (include dictionary) - with __eq__ impl",
        Benchmark("dict()", _bench_protocol(dict(), use_eq=True), range_n=100000, repeat=200),
        Benchmark(
            "cachebox.Cache(100000)",
            _bench_protocol(cachebox.Cache(100000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.Cache(100000)",
            _bench_protocol(cachetools.Cache(100000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
    ),
    "fifocache": GroupBenchmark(
        "FIFOCache",
        Benchmark(
            "cachebox.FIFOCache(10000)",
            _bench_protocol(cachebox.FIFOCache(10000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.FIFOCache(10000)",
            _bench_protocol(cachetools.FIFOCache(10000)),
            range_n=100000,
            repeat=300,
        ),
    ),
    "fifocache_eq": GroupBenchmark(
        "FIFOCache - with __eq__ impl",
        Benchmark(
            "cachebox.FIFOCache(10000)",
            _bench_protocol(cachebox.FIFOCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.FIFOCache(10000)",
            _bench_protocol(cachetools.FIFOCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
    ),
    "lrucache": GroupBenchmark(
        "LRUCache",
        Benchmark(
            "cachebox.LRUCache(10000)",
            _bench_protocol(cachebox.LRUCache(10000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.LRUCache(10000)",
            _bench_protocol(cachetools.LRUCache(10000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.LRUCache(10000)",
            _bench_protocol(cacheing.LRUCache(10000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "lru.LRU(10000)",
            _bench_protocol(lru.LRU(10000)),
            range_n=100000,
            repeat=300,
        ),
    ),
    "lrucache_eq": GroupBenchmark(
        "LRUCache - with __eq__ impl",
        Benchmark(
            "cachebox.LRUCache(10000)",
            _bench_protocol(cachebox.LRUCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.LRUCache(10000)",
            _bench_protocol(cachetools.LRUCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.LRUCache(10000)",
            _bench_protocol(cacheing.LRUCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "lru.LRU(10000)",
            _bench_protocol(lru.LRU(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
    ),
    "lfucache": GroupBenchmark(
        "LFUCache",
        Benchmark(
            "cachebox.LFUCache(10000)",
            _bench_protocol(cachebox.LFUCache(10000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.LFUCache(10000)",
            _bench_protocol(cachetools.LFUCache(10000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.LFUCache(10000)",
            _bench_protocol(cacheing.LFUCache(10000)),
            range_n=100000,
            repeat=300,
        ),
    ),
    "lfucache_eq": GroupBenchmark(
        "LFUCache - with __eq__ impl",
        Benchmark(
            "cachebox.LFUCache(10000)",
            _bench_protocol(cachebox.LFUCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.LFUCache(10000)",
            _bench_protocol(cachetools.LFUCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.LFUCache(10000)",
            _bench_protocol(cacheing.LFUCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
    ),
    "rrcache": GroupBenchmark(
        "RRCache",
        Benchmark(
            "cachebox.RRCache(10000)",
            _bench_protocol(cachebox.RRCache(10000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.RRCache(10000)",
            _bench_protocol(cachetools.RRCache(10000)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.RandomCache(10000)",
            _bench_protocol(cacheing.RandomCache(10000)),
            range_n=100000,
            repeat=300,
        ),
    ),
    "rrcache_eq": GroupBenchmark(
        "RRCache - with __eq__ impl",
        Benchmark(
            "cachebox.RRCache(10000)",
            _bench_protocol(cachebox.RRCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.RRCache(10000)",
            _bench_protocol(cachetools.RRCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.RandomCache(10000)",
            _bench_protocol(cacheing.RandomCache(10000), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
    ),
    "ttlcache": GroupBenchmark(
        "TTLCache",
        Benchmark(
            "cachebox.TTLCache(10000, 10)",
            _bench_protocol(cachebox.TTLCache(10000, 10)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.TTLCache(10000, 10)",
            _bench_protocol(cachetools.TTLCache(10000, 10)),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.TTLCache(10000, 10)",
            _bench_protocol(cacheing.TTLCache(10000, 10)),
            range_n=100000,
            repeat=300,
        ),
    ),
    "ttlcache_eq": GroupBenchmark(
        "TTLCache - with __eq__ impl",
        Benchmark(
            "cachebox.TTLCache(10000, 10)",
            _bench_protocol(cachebox.TTLCache(10000, 10), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cachetools.TTLCache(10000, 10)",
            _bench_protocol(cachetools.TTLCache(10000, 10), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.TTLCache(10000, 10)",
            _bench_protocol(cacheing.TTLCache(10000, 10), use_eq=True),
            range_n=100000,
            repeat=300,
        ),
    ),
    "vttlcache": GroupBenchmark(
        "VTTLCache",
        Benchmark(
            "cachebox.VTTLCache(100)",
            _bench_protocol(cachebox.VTTLCache(100), way="vttl_insert"),
            range_n=1000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.VTTLCache(100)",
            _bench_protocol(cacheing.VTTLCache(100), way="vttl_setitem"),
            range_n=1000,
            repeat=300,
        ),
    ),
    "vttlcache_eq": GroupBenchmark(
        "VTTLCache - with __eq__ impl",
        Benchmark(
            "cachebox.VTTLCache(100)",
            _bench_protocol(cachebox.VTTLCache(100), way="vttl_insert", use_eq=True),
            range_n=1000,
            repeat=300,
        ),
        Benchmark(
            "cacheing.VTTLCache(100)",
            _bench_protocol(cacheing.VTTLCache(100), way="vttl_setitem", use_eq=True),
            range_n=1000,
            repeat=300,
        ),
    ),
}

if len(sys.argv) != 2:
    print("python3 %s [bench name]\nAvailable benches to do:" % sys.argv[0])
    for name in benches_dict.keys():
        print("- %s" % name)

    print("- all")

    exit(0)

# Isolate CPUs for the process
if hasattr(os, "sched_setaffinity") and os.cpu_count():
    os.sched_setaffinity(0, tuple(range(os.cpu_count()))[-2:])
    print("* Isolated {} CPUs for the benchmark.".format(os.sched_getaffinity(0)))

if sys.argv[1] == "all":
    for name, b in benches_dict.items():
        b.do()
        b.plot("plots/%s.png" % name)
else:
    b = benches_dict[sys.argv[1]]
    b.do()
    b.plot("plots/%s.png" % sys.argv[1])
