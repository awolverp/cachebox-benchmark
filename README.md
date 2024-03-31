# Caching libraries Benchmarks
According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
I know, to show power of my library ...

**Qualification criteria is:**
- Needs to support minimum 2 alghoritms
- Runs on Python3.8+

If you know other library, tell me to add it to this page.

The system on which the benchmarks are done: **Linux x86_64, 8G, Intel i3-1115G4**

## Benchmarks:
**Versions**:
- cachebox version: 2.2.0
- cachetools version: 5.3.3
- cacheing version: 0.1.1

### Cache
| Benchmark        | dictionary | cachebox.Cache        | cachetools.Cache         |
|------------------|:----------:|:---------------------:|:------------------------:|
| insert 100 items | 1.99 us    | 5.56 us: 2.79x slower | 29.3 us: 14.70x slower   |
| delete           | 36.7 ns    | 144 ns: 3.93x slower  | 129 ns: 3.51x slower     |
| clear            | 5.75 ns    | 46.7 ns: 8.11x slower | 9.50 us: 1652.34x slower |
| get 100 items    | 2.24 us    | 5.38 us: 2.40x slower | 10.5 us: 4.70x slower    |
| update 100 items | 3.83 us    | 4.64 us: 1.21x slower | 33.5 us: 8.75x slower    |
| Geometric mean   | (ref)      | 3.04x slower          | 20.37x slower            |

### FIFOCache
| Benchmark         | cachebox.FIFOCache | cachetools.FIFOCache  |
|-------------------|:------------------:|:---------------------:|
| insert 1000 items | 105 us             | 906 us: 8.60x slower  |
| delete 100 items  | 146 ns             | 216 ns: 1.47x slower  |
| clear 100 items   | 46.9 ns            | 420 ns: 8.94x slower  |
| get 100 items     | 5.48 us            | 10.9 us: 1.98x slower |
| update 1000 items | 93.9 us            | 940 us: 10.01x slower |
| Geometric mean    | (ref)              | 4.68x slower          |

### LFUCache
| Benchmark         | cachebox.LFUCache | cachetools.LFUCache      | cacheing.LFUCache     |
|-------------------|:-----------------:|:------------------------:|:---------------------:|
| insert 1000 items | 606 us            | 4.24 ms: 7.00x slower    | 672 us: 1.11x slower  |
| delete            | 184 ns            | 380 ns: 2.07x slower     | 267 ns: 1.45x slower  |
| clear             | 45.9 ns           | 47.2 us: 1028.01x slower | 340 ns: 7.40x slower  |
| get 100 items     | 5.71 us           | 31.0 us: 5.42x slower    | 33.2 us: 5.81x slower |
| update 1000 items | 543 us            | 4.29 ms: 7.90x slower    | 705 us: 1.30x slower  |
| Geometric mean    | (ref)             | 14.48x slower            | 2.46x slower          |

### LRUCache
| Benchmark         | cachebox.LRUCache | cachetools.LRUCache    | cacheing.LRUCache     |
|-------------------|:-----------------:|:----------------------:|:---------------------:|
| insert 1000 items | 105 us            | 1.09 ms: 10.42x slower | 509 us: 4.86x slower  |
| delete            | 147 ns            | 216 ns: 1.47x slower   | 195 ns: 1.33x slower  |
| clear             | 45.9 ns           | 577 ns: 12.58x slower  | 212 ns: 4.63x slower  |
| get 100 items     | 5.89 us           | 25.1 us: 4.25x slower  | 15.7 us: 2.66x slower |
| update 1000 items | 93.3 us           | 1.14 ms: 12.19x slower | 542 us: 5.81x slower  |
| Geometric mean    | (ref)             | 6.31x slower           | 3.41x slower          |

### RRCache
| Benchmark         | cachebox.RRCache | cachetools.RRCache      | cacheing.RRCache      |
|-------------------|:----------------:|:-----------------------:|:---------------------:|
| insert 1000 items | 170 us           | 1.51 ms: 8.87x slower   | 831 us: 4.88x slower  |
| delete            | 144 ns           | 128 ns: 1.12x faster    | 284 ns: 1.97x slower  |
| clear             | 47.4 ns          | 24.9 us: 526.08x slower | 987 ns: 20.83x slower |
| get 100 items     | 5.38 us          | 10.8 us: 2.00x slower   | 6.66 us: 1.24x slower |
| update 1000 items | 167 us           | 1.53 ms: 9.19x slower   | 864 us: 5.18x slower  |
| Geometric mean    | (ref)            | 9.48x slower            | 4.19x slower          |

### TTLCache
| Benchmark         | cachebox.TTLCache | cachetools.TTLCache    | cacheing.TTLCache      |
|-------------------|:-----------------:|:----------------------:|:----------------------:|
| insert 1000 items | 166 us            | 3.41 ms: 20.49x slower | 1.71 ms: 10.31x slower |
| delete            | 179 ns            | 527 ns: 2.94x slower   | 570 ns: 3.18x slower   |
| clear             | 47.2 ns           | 1.94 us: 41.18x slower | 352 ns: 7.46x slower   |
| get 100 items     | 7.67 us           | 112 us: 14.66x slower  | 62.8 us: 8.19x slower  |
| update 1000 items | 121 us            | 3.44 ms: 28.32x slower | 1.76 ms: 14.49x slower |
| Geometric mean    | (ref)             | 15.94x slower          | 7.81x slower           |

### VTTLCache
| Benchmark         | cachebox.VTTLCache | cacheing.VTTLCache     |
|-------------------|:------------------:|:----------------------:|
| insert 1000 items | 1.41 ms            | 6.33 ms: 4.48x slower  |
| get 100 items     | 5.53 us            | 66.4 us: 12.00x slower |
| update 1000 items | 90.7 us            | 8.53 ms: 94.02x slower |
| Geometric mean    | (ref)              | 17.17x slower          |

> [!TIP]\
> According to this benchmark, In `cachebox.VTTLCache` if you want to insert several values in a time, use `update` instead of `insert` or `__setitem__`.

## Run yourself
use command `make <class>` to generate data-files for `<class>`; for example, we want compare `Cache` classes here:
```bash
make Cache
```

This will create data-files and show you the benchmark table.
