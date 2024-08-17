from __future__ import annotations
from benches.base import Benchmark
from benches import funcs
import os.path, os

if not os.path.exists("plots"):
    os.mkdir("plots")

benchmark = Benchmark("Cache benchmark - maxsize 1000")
benchmark.add_bench("cachetools.Cache", funcs.cachetools_Cache_bench_NoEQ)
benchmark.add_bench("cachebox.Cache", funcs.cachebox_Cache_bench_NoEQ)
benchmark.add_bench("dictionary", funcs.dictionary_bench_NoEQ)
benchmark.start()
benchmark.plot_bar("plots/cache_NoEQ.png")

benchmark = Benchmark("Cache benchmark (with __eq__ impl) - maxsize 1000")
benchmark.add_bench("cachetools.Cache", funcs.cachetools_Cache_bench_EQ)
benchmark.add_bench("cachebox.Cache", funcs.cachebox_Cache_bench_EQ)
benchmark.add_bench("dictionary", funcs.dictionary_bench_EQ)
benchmark.start()
benchmark.plot_bar("plots/cache_EQ.png")

benchmark = Benchmark("FIFO benchmark - maxsize 1000")
benchmark.add_bench("cachetools.FIFOCache", funcs.cachetools_fifo_bench_NoEQ)
benchmark.add_bench("cachebox.FIFOCache", funcs.cachebox_fifo_bench_NoEQ)
benchmark.start()
benchmark.plot_bar("plots/fifo_NoEQ.png")

benchmark = Benchmark("FIFO benchmark (with __eq__ impl) - maxsize 1000")
benchmark.add_bench("cachetools.FIFOCache", funcs.cachetools_fifo_bench_EQ)
benchmark.add_bench("cachebox.FIFOCache", funcs.cachebox_fifo_bench_EQ)
benchmark.start()
benchmark.plot_bar("plots/fifo_EQ.png")

benchmark = Benchmark("LRU benchmark - maxsize 1000")
benchmark.add_bench("cachetools.LRUCache", funcs.cachetools_lru_bench_NoEQ)
benchmark.add_bench("cachebox.LRUCache", funcs.cachebox_lru_bench_NoEQ)
benchmark.add_bench("lru.LRU", funcs.lru_lru_bench_NoEQ)
benchmark.add_bench("cacheing.LRUCache", funcs.cacheing_lru_bench_NoEQ)
benchmark.start()
benchmark.plot_bar("plots/lru_NoEQ.png")

benchmark = Benchmark("LRU benchmark (with __eq__ impl) - maxsize 1000")
benchmark.add_bench("cachetools.LRUCache", funcs.cachetools_lru_bench_EQ)
benchmark.add_bench("cachebox.LRUCache", funcs.cachebox_lru_bench_EQ)
benchmark.add_bench("lru.LRU", funcs.lru_lru_bench_EQ)
benchmark.add_bench("cacheing.LRUCache", funcs.cacheing_lru_bench_EQ)
benchmark.start()
benchmark.plot_bar("plots/lru_EQ.png")

benchmark = Benchmark("LFU benchmark - maxsize 1000")
benchmark.add_bench("cachetools.LFUCache", funcs.cachetools_lfu_bench_NoEQ)
benchmark.add_bench("cacheing.LFUCache", funcs.cacheing_lfu_bench_NoEQ)
benchmark.add_bench("cachebox.LFUCache", funcs.cachebox_lfu_bench_NoEQ)
benchmark.start()
benchmark.plot_bar("plots/lfu_NoEQ.png")

benchmark = Benchmark("LFU benchmark (with __eq__ impl) - maxsize 1000")
benchmark.add_bench("cachetools.LFUCache", funcs.cachetools_lfu_bench_EQ)
benchmark.add_bench("cacheing.LFUCache", funcs.cacheing_lfu_bench_EQ)
benchmark.add_bench("cachebox.LFUCache", funcs.cachebox_lfu_bench_EQ)
benchmark.start()
benchmark.plot_bar("plots/lfu_EQ.png")

benchmark = Benchmark("RR benchmark - maxsize 1000")
benchmark.add_bench("cachetools.RRCache", funcs.cachetools_rr_bench_NoEQ)
benchmark.add_bench("cachebox.RRCache", funcs.cachebox_rr_bench_NoEQ)
benchmark.add_bench("cacheing.RandomCache", funcs.cacheing_rr_bench_NoEQ)
benchmark.start()
benchmark.plot_bar("plots/rr_NoEQ.png")

benchmark = Benchmark("RR benchmark (with __eq__ impl) - maxsize 1000")
benchmark.add_bench("cachetools.RRCache", funcs.cachetools_rr_bench_EQ)
benchmark.add_bench("cachebox.RRCache", funcs.cachebox_rr_bench_EQ)
benchmark.add_bench("cacheing.RandomCache", funcs.cacheing_rr_bench_EQ)
benchmark.start()
benchmark.plot_bar("plots/rr_EQ.png")

benchmark = Benchmark("TTL benchmark - maxsize 1000")
benchmark.add_bench("cachetools.TTLCache", funcs.cachetools_ttl_bench_NoEQ)
benchmark.add_bench("cachebox.TTLCache", funcs.cachebox_ttl_bench_NoEQ)
benchmark.add_bench("cacheing.TTLCache", funcs.cacheing_ttl_bench_NoEQ)
benchmark.start()
benchmark.plot_bar("plots/ttl_NoEQ.png")

benchmark = Benchmark("TTL benchmark (with __eq__ impl) - maxsize 1000")
benchmark.add_bench("cachetools.TTLCache", funcs.cachetools_ttl_bench_EQ)
benchmark.add_bench("cachebox.TTLCache", funcs.cachebox_ttl_bench_EQ)
benchmark.add_bench("cacheing.TTLCache", funcs.cacheing_ttl_bench_EQ)
benchmark.start()
benchmark.plot_bar("plots/ttl_EQ.png")

benchmark = Benchmark("VTTL benchmark - maxsize 1000")
benchmark.add_bench("cachebox.VTTLCache", funcs.cachebox_vttl_bench_NoEQ)
benchmark.add_bench("cacheing.VTTLCache", funcs.cacheing_vttl_bench_NoEQ)
benchmark.start()
benchmark.plot_bar("plots/vttl_NoEQ.png")

benchmark = Benchmark("VTTL benchmark (with __eq__ impl) - maxsize 1000")
benchmark.add_bench("cachebox.VTTLCache", funcs.cachebox_vttl_bench_EQ)
benchmark.add_bench("cacheing.VTTLCache", funcs.cacheing_vttl_bench_EQ)
benchmark.start()
benchmark.plot_bar("plots/vttl_EQ.png")
