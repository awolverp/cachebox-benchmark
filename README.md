# Caching libraries Benchmarks
According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...

**Qualification criteria is:**
- Needs to support minimum 5 alghoritms
- Runs on Python3.8 and above

If you know other library, tell me to add it to this page.

> [!NOTE]\
> The system on which the benchmarks are done: **Linux x86_64, 8G, Intel i3-1115G4**

## Benchmarks:
**Versions**:
- cachebox version: 3.2.1
- cachetools version: 5.3.3
- cacheing version: 0.1.1

### Cache
| Benchmark        | dictionary | cachebox.Cache        | cachetools.Cache       |
|------------------|:----------:|:---------------------:|:----------------------:|
| insert 100 items | 1.91 us    | 5.36 us: 2.81x slower | 32.7 us: 17.13x slower |
| delete           | 46.3 ns    | 149 ns: 3.22x slower  | 148 ns: 3.19x slower   |
| get 100 items    | 2.07 us    | 5.40 us: 2.61x slower | 11.3 us: 5.47x slower  |
| update 100 items | 3.70 us    | 4.14 us: 1.12x slower | 36.9 us: 9.96x slower  |
| Geometric mean   | (ref)      | 2.27x slower          | 7.39x slower           |

### FIFOCache
| Benchmark         | cachebox.FIFOCache | cachetools.FIFOCache   |
|-------------------|:------------------:|:----------------------:|
| insert 1000 items | 92.5 us            | 1.02 ms: 11.01x slower |
| delete            | 155 ns             | 254 ns: 1.63x slower   |
| get 100 items     | 5.37 us            | 11.2 us: 2.09x slower  |
| update 1000 items | 77.5 us            | 1.08 ms: 13.98x slower |
| Geometric mean    | (ref)              | 4.79x slower           |

### LFUCache
| Benchmark         | cachebox.LFUCache | cachetools.LFUCache    | cacheing.LFUCache     |
|-------------------|:-----------------:|:----------------------:|:---------------------:|
| insert 1000 items | 335 us            | 4.93 ms: 14.72x slower | 726 us: 2.17x slower  |
| delete            | 148 ns            | 391 ns: 2.64x slower   | 316 ns: 2.13x slower  |
| get 100 items     | 5.44 us           | 38.1 us: 7.00x slower  | 35.7 us: 6.57x slower |
| update 1000 items | 298 us            | 4.96 ms: 16.63x slower | 765 us: 2.56x slower  |
| Geometric mean    | (ref)             | 8.20x slower           | 2.97x slower          |

### LRUCache
| Benchmark         | cachebox.LRUCache | cachetools.LRUCache    | cacheing.LRUCache     |
|-------------------|:-----------------:|:----------------------:|:---------------------:|
| insert 1000 items | 94.5 us           | 1.33 ms: 14.05x slower | 557 us: 5.90x slower  |
| delete            | 158 ns            | 253 ns: 1.60x slower   | 229 ns: 1.45x slower  |
| get 100 items     | 6.18 us           | 29.0 us: 4.69x slower  | 15.9 us: 2.57x slower |
| update 1000 items | 77.0 us           | 1.38 ms: 17.94x slower | 596 us: 7.74x slower  |
| Geometric mean    | (ref)             | 6.60x slower           | 3.61x slower          |

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
| insert 1000 items | 146 us            | 3.26 ms: 22.30x slower | 1.80 ms: 12.34x slower |
| delete            | 181 ns            | 522 ns: 2.89x slower   | 632 ns: 3.50x slower   |
| get 100 items     | 7.31 us           | 94.6 us: 12.94x slower | 67.5 us: 9.23x slower  |
| update 1000 items | 102 us            | 3.31 ms: 32.63x slower | 1.84 ms: 18.14x slower |
| Geometric mean    | (ref)             | 12.84x slower          | 9.22x slower           |

### VTTLCache
| Benchmark         | cachebox.VTTLCache | cacheing.VTTLCache      |
|-------------------|:------------------:|:-----------------------:|
| insert 1000 items | 729 us             | 6.87 ms: 9.43x slower   |
| get 100 items     | 5.47 us            | 67.5 us: 12.34x slower  |
| update 1000 items | 90.5 us            | 9.19 ms: 101.58x slower |
| Geometric mean    | (ref)              | 22.78x slower           |

> [!TIP]\
> According to this benchmark, In `cachebox.VTTLCache` if you want to insert several values in a time, use `update` instead of `insert` or `__setitem__`.

## Run yourself
use command `make <class>` to generate data-files for `<class>`; for example, we want compare `Cache` classes here:
```bash
make Cache
```

This will create data-files and show you the benchmark table.

## Notes

**Note about cacheout**\
We removed **cacheout** library from benchmark because that's very slow;

**Note about theine**\
We didn't add **theine** because it don't have many methods and operations
and only has 3 policies. We only compare a LRU policy for you to see speeds:

```sh
$ python3 -m timeit -s 'import theine; c = theine.Cache("lru", 1000)' 'for i in range(1000): c.set(i, i)'
500 loops, best of 5: 462 usec per loop

$ python3 -m timeit -s 'import cachebox; c = cachebox.LRUCache(1000)' 'for i in range(1000): c.insert(i, i)'
2000 loops, best of 5: 118 usec per loop
```

And it has high memory usage that is not good for a caching library ...
