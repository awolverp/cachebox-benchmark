from .base import Bencher
import cachetools
import cachebox
import cacheing
import lru
import random


SIZE = 1000
RANDOM_TTL = random.random() * 2


def _simple_benchmark_cache(obj: type, maxsize=("maxsize", SIZE), rng: int = SIZE, **kwargs):
    def wrapper(b: Bencher):
        kwargs[maxsize[0]] = maxsize[1]
        cache = obj(**kwargs)

        i_range = range(rng)

        b.start()
        for i in i_range:
            cache[i] = i
        b.stop()
    
    return wrapper

# region Cache

dictionary_bench = _simple_benchmark_cache(dict)

cachebox_Cache_bench = _simple_benchmark_cache(cachebox.Cache)

cachetools_Cache_bench = _simple_benchmark_cache(cachetools.Cache)

# endregion
# region FIFO

cachebox_fifo_bench = _simple_benchmark_cache(cachebox.FIFOCache, rng=SIZE*10)

cachetools_fifo_bench = _simple_benchmark_cache(cachetools.FIFOCache, rng=SIZE*10)

# endregion
# region LRU

cachebox_lru_bench = _simple_benchmark_cache(cachebox.LRUCache, rng=SIZE*10)

cachetools_lru_bench = _simple_benchmark_cache(cachetools.LRUCache, rng=SIZE*10)

cacheing_lru_bench = _simple_benchmark_cache(cacheing.LRUCache, ("capacity", SIZE), rng=SIZE*10)

lru_lru_bench = _simple_benchmark_cache(lru.LRU, ("size", SIZE), rng=SIZE*10)

# endregion
# region LFU

cachebox_lfu_bench = _simple_benchmark_cache(cachebox.LFUCache, rng=SIZE*10)

cachetools_lfu_bench = _simple_benchmark_cache(cachetools.LFUCache, rng=SIZE*10)

cacheing_lfu_bench = _simple_benchmark_cache(cacheing.LFUCache, ("capacity", SIZE), rng=SIZE*10)

# endregion
# region RR

cachebox_rr_bench = _simple_benchmark_cache(cachebox.RRCache, rng=SIZE*10)

cachetools_rr_bench = _simple_benchmark_cache(cachetools.RRCache, rng=SIZE*10)

cacheing_rr_bench = _simple_benchmark_cache(cacheing.RandomCache, ("capacity", SIZE), rng=SIZE*10)

# endregion
# region TTL

cachebox_ttl_bench = _simple_benchmark_cache(cachebox.TTLCache, rng=SIZE*10, ttl=RANDOM_TTL)

cachetools_ttl_bench = _simple_benchmark_cache(cachetools.TTLCache, rng=SIZE*10, ttl=RANDOM_TTL)

cacheing_ttl_bench = _simple_benchmark_cache(cacheing.TTLCache, ("capacity", SIZE), rng=SIZE*10, ttl=RANDOM_TTL)

# endregion
# region VTTL

def cachebox_vttl_bench(b: Bencher):
    cache = cachebox.VTTLCache(SIZE)

    i_range = range(SIZE*10)

    b.start()
    for i in i_range:
        cache.insert(i, i, RANDOM_TTL)
    b.stop()

def cacheing_vttl_bench(b: Bencher):
    cache = cacheing.VTTLCache(SIZE)

    i_range = range(SIZE*10)

    b.start()
    for i in i_range:
        cache[(i, RANDOM_TTL)] = i
    b.stop()

# endregion
