# Caching libraries Benchmarks
According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
I know, to show power of my library ...

**Qualification criteria is:**
- Needs to support minimum 5 alghoritms
- Runs on Python3.8 and above

If you know other library, tell me to add it to this page.

> [!NOTE]\
> The system on which the benchmarks are done: **Linux x86_64, 8G, Intel i3-1115G4**


## Benchmarks:
**Versions**:
- cachebox version: 2.2.2
- cachetools version: 5.3.3
- cacheing version: 0.1.1
- cacheout version: 0.16.0

### Cache
| Benchmark        | dictionary | cachebox.Cache        | cachetools.Cache       | cacheout.Cache         |
|------------------|:----------:|:---------------------:|:----------------------:|:----------------------:|
| insert 100 items | 1.97 us    | 5.26 us: 2.68x slower | 28.9 us: 14.72x slower | 71.8 us: 36.49x slower |
| delete           | 36.3 ns    | 146 ns: 4.02x slower  | 129 ns: 3.54x slower   | 616 ns: 16.96x slower  |
| get 100 items    | 2.22 us    | 5.42 us: 2.44x slower | 10.5 us: 4.73x slower  | 52.6 us: 23.70x slower |
| update 100 items | 3.73 us    | 4.01 us: 1.08x slower | 33.3 us: 8.94x slower  | 64.4 us: 17.29x slower |
| Geometric mean   | (ref)      | 2.30x slower          | 6.85x slower           | 22.44x slower          |

### FIFOCache
| Benchmark         | cachebox.FIFOCache | cachetools.FIFOCache  | cacheout.FIFOCache     |
|-------------------|:------------------:|:---------------------:|:----------------------:|
| insert 1000 items | 106 us             | 904 us: 8.53x slower  | 2.36 ms: 22.24x slower |
| delete            | 150 ns             | 215 ns: 1.44x slower  | 584 ns: 3.90x slower   |
| get 100 items     | 5.48 us            | 10.8 us: 1.97x slower | 52.2 us: 9.52x slower  |
| update 1000 items | 85.6 us            | 942 us: 11.00x slower | 2.74 ms: 31.96x slower |
| Geometric mean    | (ref)              | 4.04x slower          | 12.75x slower          |

### LFUCache
| Benchmark         | cachebox.LFUCache | cachetools.LFUCache   | cacheing.LFUCache     | cacheout.LFUCache      |
|-------------------|:-----------------:|:---------------------:|:---------------------:|:----------------------:|
| insert 1000 items | 584 us            | 4.34 ms: 7.43x slower | 668 us: 1.14x slower  | 6.55 ms: 11.21x slower |
| delete            | 191 ns            | 380 ns: 1.99x slower  | 268 ns: 1.40x slower  | 4.75 us: 24.85x slower |
| get 100 items     | 5.63 us           | 31.0 us: 5.52x slower | 33.0 us: 5.87x slower | 101 us: 17.97x slower  |
| update 1000 items | 551 us            | 4.30 ms: 7.80x slower | 702 us: 1.27x slower  | 7.02 ms: 12.74x slower |
| Geometric mean    | (ref)             | 5.02x slower          | 1.86x slower          | 15.89x slower          |

### LRUCache
| Benchmark         | cachebox.LRUCache | cachetools.LRUCache    | cacheing.LRUCache     | cacheout.LRUCache      |
|-------------------|:-----------------:|:----------------------:|:---------------------:|:----------------------:|
| insert 1000 items | 103 us            | 1.09 ms: 10.58x slower | 507 us: 4.90x slower  | 2.33 ms: 22.51x slower |
| delete            | 148 ns            | 215 ns: 1.46x slower   | 190 ns: 1.28x slower  | 600 ns: 4.06x slower   |
| get 100 items     | 5.81 us           | 25.1 us: 4.32x slower  | 15.4 us: 2.65x slower | 81.5 us: 14.02x slower |
| update 1000 items | 85.4 us           | 1.13 ms: 13.22x slower | 542 us: 6.35x slower  | 2.76 ms: 32.33x slower |
| Geometric mean    | (ref)             | 5.45x slower           | 3.21x slower          | 14.27x slower          |

### RRCache
| Benchmark         | cachebox.RRCache | cachetools.RRCache     | cacheing.RRCache      | cacheout.RRCache       |
|-------------------|:----------------:|:----------------------:|:---------------------:|:----------------------:|
| insert 1000 items | 160 us           | 1.52 ms: 9.45x slower  | 827 us: 5.15x slower  | 4.73 ms: 29.47x slower |
| delete            | 146 ns           | 129 ns: 1.14x faster   | 284 ns: 1.94x slower  | 3.99 us: 27.28x slower |
| get 100 items     | 5.43 us          | 10.8 us: 1.98x slower  | 6.69 us: 1.23x slower | 52.1 us: 9.59x slower  |
| update 1000 items | 150 us           | 1.53 ms: 10.19x slower | 861 us: 5.72x slower  | 5.31 ms: 35.27x slower |
| Geometric mean    | (ref)            | 3.60x slower           | 2.90x slower          | 22.83x slower          |

### TTLCache
| Benchmark         | cachebox.TTLCache | cachetools.TTLCache    | cacheing.TTLCache      | cacheout.TTLCache      |
|-------------------|:-----------------:|:----------------------:|:----------------------:|:----------------------:|
| insert 1000 items | 163 us            | 3.42 ms: 21.02x slower | 1.71 ms: 10.54x slower | 5.50 ms: 33.78x slower |
| delete            | 179 ns            | 527 ns: 2.94x slower   | 570 ns: 3.18x slower   | very very slow ...     |
| get 100 items     | 7.54 us           | 113 us: 14.94x slower  | 63.1 us: 8.37x slower  | 38.7 us: 5.13x slower  |
| update 1000 items | 116 us            | 3.47 ms: 30.02x slower | 1.78 ms: 15.38x slower | 6.02 ms: 52.06x slower |
| Geometric mean    | (ref)             | 21.13x slower          | 11.07x slower          | 20.82x slower          |

### VTTLCache
| Benchmark         | cachebox.VTTLCache | cacheing.VTTLCache      | cacheout.VTTLCache     |
|-------------------|:------------------:|:-----------------------:|:----------------------:|
| insert 1000 items | 1.41 ms            | 6.40 ms: 4.55x slower   | 5.85 ms: 4.16x slower  |
| get 100 items     | 5.60 us            | 63.3 us: 11.30x slower  | 52.2 us: 9.32x slower  |
| update 1000 items | 82.0 us            | 8.41 ms: 102.62x slower | 5.91 ms: 72.12x slower |
| Geometric mean    | (ref)              | 17.41x slower           | 14.09x slower          |

> [!TIP]\
> According to this benchmark, In `cachebox.VTTLCache` if you want to insert several values in a time, use `update` instead of `insert` or `__setitem__`.

## Run yourself
use command `make <class>` to generate data-files for `<class>`; for example, we want compare `Cache` classes here:
```bash
make Cache
```

This will create data-files and show you the benchmark table.
