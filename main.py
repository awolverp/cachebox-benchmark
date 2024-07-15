from __future__ import annotations
from benches.base import Benchmark
from benches import funcs
import os.path, os

if not os.path.exists("plots"):
    os.mkdir("plots")

benchmark = Benchmark("Cache benchmark - maxsize 1000")
benchmark.add_bench("cachetools.Cache", funcs.cachetools_Cache_bench)
benchmark.add_bench("cachebox.Cache", funcs.cachebox_Cache_bench)
benchmark.add_bench("dictionary", funcs.dictionary_bench)
benchmark.start()
benchmark.plot_bar("plots/cache.png")

benchmark = Benchmark("FIFO benchmark - maxsize 1000")
benchmark.add_bench("cachetools.FIFOCache", funcs.cachetools_fifo_bench)
benchmark.add_bench("cachebox.FIFOCache", funcs.cachebox_fifo_bench)
benchmark.start()
benchmark.plot_bar("plots/fifo.png")

benchmark = Benchmark("LRU benchmark - maxsize 1000")
benchmark.add_bench("cachetools.LRUCache", funcs.cachetools_lru_bench)
benchmark.add_bench("cachebox.LRUCache", funcs.cachebox_lru_bench)
benchmark.add_bench("lru.LRU", funcs.lru_lru_bench)
benchmark.add_bench("cacheing.LRUCache", funcs.cacheing_lru_bench)
benchmark.start()
benchmark.plot_bar("plots/lru.png")

benchmark = Benchmark("LFU benchmark - maxsize 1000")
benchmark.add_bench("cachetools.LFUCache", funcs.cachetools_lfu_bench)
benchmark.add_bench("cacheing.LFUCache", funcs.cacheing_lfu_bench)
benchmark.add_bench("cachebox.LFUCache", funcs.cachebox_lfu_bench)
benchmark.start()
benchmark.plot_bar("plots/lfu.png")

benchmark = Benchmark("RR benchmark - maxsize 1000")
benchmark.add_bench("cachetools.RRCache", funcs.cachetools_rr_bench)
benchmark.add_bench("cachebox.RRCache", funcs.cachebox_rr_bench)
benchmark.add_bench("cacheing.RandomCache", funcs.cacheing_rr_bench)
benchmark.start()
benchmark.plot_bar("plots/rr.png")

benchmark = Benchmark("TTL benchmark - maxsize 1000")
benchmark.add_bench("cachetools.TTLCache", funcs.cachetools_ttl_bench)
benchmark.add_bench("cachebox.TTLCache", funcs.cachebox_ttl_bench)
benchmark.add_bench("cacheing.TTLCache", funcs.cacheing_ttl_bench)
benchmark.start()
benchmark.plot_bar("plots/ttl.png")

benchmark = Benchmark("VTTL benchmark - maxsize 1000")
benchmark.add_bench("cachebox.VTTLCache", funcs.cachebox_vttl_bench)
benchmark.add_bench("cacheing.VTTLCache", funcs.cacheing_vttl_bench)
benchmark.start()
benchmark.plot_bar("plots/vttl.png")
