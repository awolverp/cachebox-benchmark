# Caching libraries Benchmarks
According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
I know, to show power of my library ...

**Qualification criteria is:**
- Needs to support minimum 5 alghoritms
- Runs on Python3.8 and above

If you know other library, tell me to add it to this page.

> [!NOTE]\
> The system on which the benchmarks are done: **Linux x86_64, 8G, Intel i3-1115G4**

> [!NOTE]\
> We removed **cacheout** library from benchmark because that's very slow;
> I will add **theine** instead of that.

## Benchmarks:
**Versions**:
- cachebox version: 3.0.0
- cachetools version: 5.3.3
- cacheing version: 0.1.1

### Cache
| Benchmark        | dictionary | cachebox.Cache        | cachetools.Cache       |
|------------------|:----------:|:---------------------:|:----------------------:|
| insert 100 items | 1.93 us    | 5.49 us: 2.84x slower | 32.5 us: 16.81x slower |
| delete           | 46.2 ns    | 147 ns: 3.19x slower  | 149 ns: 3.22x slower   |
| get 100 items    | 2.05 us    | 5.36 us: 2.62x slower | 11.5 us: 5.60x slower  |
| update 100 items | 3.66 us    | 4.19 us: 1.14x slower | 37.1 us: 10.13x slower |
| Geometric mean   | (ref)      | 2.28x slower          | 7.44x slower           |

### FIFOCache
| Benchmark         | cachebox.FIFOCache | cachetools.FIFOCache   |
|-------------------|:------------------:|:----------------------:|
| insert 1000 items | 88.9 us            | 1.03 ms: 11.55x slower |
| delete            | 159 ns             | 256 ns: 1.61x slower   |
| get 100 items     | 5.40 us            | 11.5 us: 2.13x slower  |
| update 1000 items | 71.9 us            | 1.09 ms: 15.11x slower |
| Geometric mean    | (ref)              | 4.95x slower           |

### LFUCache
| Benchmark         | cachebox.LFUCache | cacheing.LFUCache     | cachetools.LFUCache    |
|-------------------|:-----------------:|:---------------------:|:----------------------:|
| insert 1000 items | 320 us            | 729 us: 2.28x slower  | 4.90 ms: 15.29x slower |
| delete            | 148 ns            | 322 ns: 2.17x slower  | 399 ns: 2.69x slower   |
| get 100 items     | 5.41 us           | 35.9 us: 6.63x slower | 38.3 us: 7.07x slower  |
| update 1000 items | 285 us            | 770 us: 2.71x slower  | 4.93 ms: 17.32x slower |
| Geometric mean    | (ref)             | 3.07x slower          | 8.42x slower           |

### LRUCache
| Benchmark         | cachebox.LRUCache | cachetools.LRUCache    | cacheing.LRUCache     |
|-------------------|:-----------------:|:----------------------:|:---------------------:|
| insert 1000 items | 86.0 us           | 1.28 ms: 14.93x slower | 561 us: 6.52x slower  |
| delete            | 157 ns            | 257 ns: 1.64x slower   | 232 ns: 1.48x slower  |
| get 100 items     | 6.28 us           | 29.2 us: 4.65x slower  | 15.9 us: 2.54x slower |
| update 1000 items | 70.6 us           | 1.33 ms: 18.82x slower | 597 us: 8.46x slower  |
| Geometric mean    | (ref)             | 6.80x slower           | 3.79x slower          |

### RRCache
| Benchmark         | cachebox.RRCache | cachetools.RRCache     | cacheing.RRCache      |
|-------------------|:----------------:|:----------------------:|:---------------------:|
| insert 1000 items | 163 us           | 1.65 ms: 10.13x slower | 928 us: 5.69x slower  |
| delete            | 149 ns           | not significant        | 354 ns: 2.38x slower  |
| get 100 items     | 5.40 us          | 11.3 us: 2.10x slower  | 6.26 us: 1.16x slower |
| update 1000 items | 153 us           | 1.74 ms: 11.35x slower | 985 us: 6.43x slower  |
| Geometric mean    | (ref)            | 3.94x slower           | 3.17x slower          |

### TTLCache
| Benchmark         | cachebox.TTLCache | cachetools.TTLCache    | cacheing.TTLCache      |
|-------------------|:-----------------:|:----------------------:|:----------------------:|
| insert 1000 items | 139 us            | 3.25 ms: 23.35x slower | 1.82 ms: 13.07x slower |
| delete            | 181 ns            | 528 ns: 2.92x slower   | 637 ns: 3.53x slower   |
| get 100 items     | 7.29 us           | 95.7 us: 13.12x slower | 68.6 us: 9.42x slower  |
| update 1000 items | 92.9 us           | 3.36 ms: 36.18x slower | 1.89 ms: 20.33x slower |
| Geometric mean    | (ref)             | 13.42x slower          | 9.69x slower           |

### VTTLCache
| Benchmark         | cachebox.VTTLCache | cacheing.VTTLCache      |
|-------------------|:------------------:|:-----------------------:|
| insert 1000 items | 693 us             | 6.86 ms: 9.91x slower   |
| get 100 items     | 5.49 us            | 68.4 us: 12.45x slower  |
| update 1000 items | 86.0 us            | 9.19 ms: 106.91x slower |
| Geometric mean    | (ref)              | 23.63x slower           |

> [!TIP]\
> According to this benchmark, In `cachebox.VTTLCache` if you want to insert several values in a time, use `update` instead of `insert` or `__setitem__`.

## Run yourself
use command `make <class>` to generate data-files for `<class>`; for example, we want compare `Cache` classes here:
```bash
make Cache
```

This will create data-files and show you the benchmark table.
