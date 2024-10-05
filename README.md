# Caching libraries Benchmarks
According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...

If you know other library, tell me to add it to this page.

> [!NOTE]\
> The system on which the benchmarks are done: **Manjaro Linux x86_64, 8G, Intel i3-1115G4**

## Benchmarks:
**Versions**:
- Python: 3.12.5
- cachebox version: 4.2.0
- cachetools version: 5.5.0
- cacheing version: 0.1.1
- lru-dict: 1.3.0

## Cache

![cache-image](plots/cache_NoEQ.png)

![cache-image](plots/cache_EQ.png)

## FIFOCache

![fifo-image](plots/fifo_NoEQ.png)

![fifo-image](plots/fifo_EQ.png)

## LFUCache

![lfu-image](plots/lfu_NoEQ.png)

![lfu-image](plots/lfu_EQ.png)

## LRUCache

![lru-image](plots/lru_NoEQ.png)

![lru-image](plots/lru_EQ.png)

## RRCache

![rr-image](plots/rr_NoEQ.png)

![rr-image](plots/rr_EQ.png)

## TTLCache

![ttl-image](plots/ttl_NoEQ.png)

![ttl-image](plots/ttl_EQ.png)

## VTTLCache

![vttl-image](plots/vttl_NoEQ.png)

![vttl-image](plots/vttl_EQ.png)
