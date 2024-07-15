# Caching libraries Benchmarks
According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...

If you know other library, tell me to add it to this page.

> [!NOTE]\
> The system on which the benchmarks are done: **Linux x86_64, 8G, Intel i3-1115G4**

## Benchmarks:
**Versions**:
- Python: 3.12.4
- cachebox version: 3.4.0
- cachetools version: 5.3.3
- cacheing version: 0.1.1
- lru-dict: 1.3.0

![cache-image](plots/cache.png)

![fifo-image](plots/fifo.png)

![lru-image](plots/lru.png)

![rr-image](plots/rr.png)

![lfu-image](plots/lfu.png)

![ttl-image](plots/ttl.png)

![vttl-image](plots/vttl.png)
