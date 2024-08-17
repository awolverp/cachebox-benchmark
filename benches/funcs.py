from .base import Bencher
import cachetools
import cachebox
import cacheing
import lru
import random

import dataclasses

@dataclasses.dataclass
class EQ:
    def __init__(self, val: int) -> None:
        self.val = val

    def __eq__(self, other: "EQ") -> bool:
        return hash(self.val) == hash(other.val) and other.val == self.val

    def __hash__(self) -> int:
        return self.val

@dataclasses.dataclass
class NoEQ:
    def __init__(self, val: int) -> None:
        self.val = val

    def __hash__(self) -> int:
        return self.val


SIZE = 1000
RANDOM_TTL = random.random() * 2


def _simple_benchmark_cache(obj: type, func, maxsize=("maxsize", SIZE), rng: int = SIZE, **kwargs):
    def wrapper(b: Bencher):
        kwargs[maxsize[0]] = maxsize[1]
        cache = obj(**kwargs)

        i_range = range(rng)

        b.start()
        for i in i_range:
            cache[func(i)] = func(i)
            cache.get(func(i), None)
        b.stop()
    
    return wrapper

# region Cache

dictionary_bench_NoEQ = _simple_benchmark_cache(dict, NoEQ)

cachebox_Cache_bench_NoEQ = _simple_benchmark_cache(cachebox.Cache, NoEQ)

cachetools_Cache_bench_NoEQ = _simple_benchmark_cache(cachetools.Cache, NoEQ)

dictionary_bench_EQ = _simple_benchmark_cache(dict, EQ)

cachebox_Cache_bench_EQ = _simple_benchmark_cache(cachebox.Cache, EQ)

cachetools_Cache_bench_EQ = _simple_benchmark_cache(cachetools.Cache, EQ)

# endregion
# region FIFO

cachebox_fifo_bench_NoEQ = _simple_benchmark_cache(cachebox.FIFOCache, NoEQ, rng=SIZE*10)

cachetools_fifo_bench_NoEQ = _simple_benchmark_cache(cachetools.FIFOCache, NoEQ, rng=SIZE*10)

cachebox_fifo_bench_EQ = _simple_benchmark_cache(cachebox.FIFOCache, EQ, rng=SIZE*10)

cachetools_fifo_bench_EQ = _simple_benchmark_cache(cachetools.FIFOCache, EQ, rng=SIZE*10)

# endregion
# region LRU

cachebox_lru_bench_NoEQ = _simple_benchmark_cache(cachebox.LRUCache, NoEQ, rng=SIZE*10)

cachetools_lru_bench_NoEQ = _simple_benchmark_cache(cachetools.LRUCache, NoEQ, rng=SIZE*10)

cacheing_lru_bench_NoEQ = _simple_benchmark_cache(cacheing.LRUCache, NoEQ, ("capacity", SIZE), rng=SIZE*10)

lru_lru_bench_NoEQ = _simple_benchmark_cache(lru.LRU, NoEQ, ("size", SIZE), rng=SIZE*10)

cachebox_lru_bench_EQ = _simple_benchmark_cache(cachebox.LRUCache, EQ, rng=SIZE*10)

cachetools_lru_bench_EQ = _simple_benchmark_cache(cachetools.LRUCache, EQ, rng=SIZE*10)

cacheing_lru_bench_EQ = _simple_benchmark_cache(cacheing.LRUCache, EQ, ("capacity", SIZE), rng=SIZE*10)

lru_lru_bench_EQ = _simple_benchmark_cache(lru.LRU, EQ, ("size", SIZE), rng=SIZE*10)

# endregion
# region LFU

cachebox_lfu_bench_NoEQ = _simple_benchmark_cache(cachebox.LFUCache, NoEQ, rng=SIZE*10)

cachetools_lfu_bench_NoEQ = _simple_benchmark_cache(cachetools.LFUCache, NoEQ, rng=SIZE*10)

cacheing_lfu_bench_NoEQ = _simple_benchmark_cache(cacheing.LFUCache, NoEQ, ("capacity", SIZE), rng=SIZE*10)

cachebox_lfu_bench_EQ = _simple_benchmark_cache(cachebox.LFUCache, EQ, rng=SIZE*10)

cachetools_lfu_bench_EQ = _simple_benchmark_cache(cachetools.LFUCache, EQ, rng=SIZE*10)

cacheing_lfu_bench_EQ = _simple_benchmark_cache(cacheing.LFUCache, EQ, ("capacity", SIZE), rng=SIZE*10)

# endregion
# region RR

cachebox_rr_bench_EQ = _simple_benchmark_cache(cachebox.RRCache, EQ, rng=SIZE*10)

cachetools_rr_bench_EQ = _simple_benchmark_cache(cachetools.RRCache, EQ, rng=SIZE*10)

cacheing_rr_bench_EQ = _simple_benchmark_cache(cacheing.RandomCache, EQ, ("capacity", SIZE), rng=SIZE*10)

cachebox_rr_bench_NoEQ = _simple_benchmark_cache(cachebox.RRCache, NoEQ, rng=SIZE*10)

cachetools_rr_bench_NoEQ = _simple_benchmark_cache(cachetools.RRCache, NoEQ, rng=SIZE*10)

cacheing_rr_bench_NoEQ = _simple_benchmark_cache(cacheing.RandomCache, NoEQ, ("capacity", SIZE), rng=SIZE*10)

# endregion
# # region TTL

cachebox_ttl_bench_EQ = _simple_benchmark_cache(cachebox.TTLCache, EQ, rng=SIZE*10, ttl=RANDOM_TTL)

cachetools_ttl_bench_EQ = _simple_benchmark_cache(cachetools.TTLCache, EQ, rng=SIZE*10, ttl=RANDOM_TTL)

cacheing_ttl_bench_EQ = _simple_benchmark_cache(cacheing.TTLCache, EQ, ("capacity", SIZE), rng=SIZE*10, ttl=RANDOM_TTL)

cachebox_ttl_bench_NoEQ = _simple_benchmark_cache(cachebox.TTLCache, NoEQ, rng=SIZE*10, ttl=RANDOM_TTL)

cachetools_ttl_bench_NoEQ = _simple_benchmark_cache(cachetools.TTLCache, NoEQ, rng=SIZE*10, ttl=RANDOM_TTL)

cacheing_ttl_bench_NoEQ = _simple_benchmark_cache(cacheing.TTLCache, NoEQ, ("capacity", SIZE), rng=SIZE*10, ttl=RANDOM_TTL)


# endregion
# region VTTL

def cachebox_vttl_bench_NoEQ(b: Bencher):
    cache = cachebox.VTTLCache(SIZE)

    i_range = range(SIZE*10)

    b.start()
    for i in i_range:
        cache.insert(NoEQ(i), i, RANDOM_TTL)
        cache.get(NoEQ(i))
    b.stop()

def cacheing_vttl_bench_NoEQ(b: Bencher):
    cache = cacheing.VTTLCache(SIZE)

    i_range = range(SIZE*10)

    b.start()
    for i in i_range:
        cache[(NoEQ(i), RANDOM_TTL)] = i
        cache[NoEQ(i)]
    b.stop()

def cachebox_vttl_bench_EQ(b: Bencher):
    cache = cachebox.VTTLCache(SIZE)

    i_range = range(SIZE*10)

    b.start()
    for i in i_range:
        cache.insert(EQ(i), i, RANDOM_TTL)
        cache.get(EQ(i))
    b.stop()

def cacheing_vttl_bench_EQ(b: Bencher):
    cache = cacheing.VTTLCache(SIZE)

    i_range = range(SIZE*10)

    b.start()
    for i in i_range:
        cache[(EQ(i), RANDOM_TTL)] = i
        cache[EQ(i)]
    b.stop()

# endregion
