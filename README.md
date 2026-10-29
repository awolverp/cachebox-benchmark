# Caching libraries Benchmarks

According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...

If you know other library, tell me to add it to this page.

> [!NOTE]\
> The `cacheing.VTTLCache` class was excluded from the benchmark because assigning a key raises `TypeError`.

## Methodology

Times are **from Python**: each sample is a calibrated inner loop around a single API call (`set` / `get` / `delete` / `popitem`). Setup and teardown are not timed. GC is collected before each sample and disabled during the timed region.

Reported values are the **median** ns/op (tables ranked by median), plus mean, stdev, MAD, ops/sec, sample count, and coefficient of variation. Outliers are **not** dropped. A result is flagged when CV > 10% or max > 1.5× mean.

All implementations use the same working set (`maxsize = 4096`, integer keys/values). TTL caches are constructed with a 3600s TTL so nothing expires during a sample. `dict`, `cachebox.Cache`, and `cachetools.Cache` have no eviction policy and are skipped on eviction cases.

| Case                       | What is measured                                                      |
| -------------------------- | --------------------------------------------------------------------- |
| Set new (no eviction)      | Insert keys that are not present and do not evict (cache ~25% full).  |
| Set at capacity (eviction) | Insert new keys into a cache already at maxsize.                      |
| Lookup existing            | `get` of a present key (LRU/LFU recency/frequency updates included).  |
| Lookup missing             | `get` of a missing key.                                               |
| Deletion                   | Delete present keys (one delete per populated key, then a new cache). |
| Popitem                    | `popitem()` on a cache filled to maxsize.                             |
| Hash collision             | `get` of keys whose `hash()` is always 42.                            |

moka-py is a concurrent Rust cache measured **single-threaded** like the others.

## 🖥️ System Information

- **Platform**: Linux-7.2.11-arch1-1-x86_64-with-glibc2.44
- **Python**: 3.14.8
- **Processor**: 11th Gen Intel(R) Core(TM) i3-1115G4 @ 3.00GHz
- **Timer**: resolution 350.0 ns, overhead 42.0 ns
- **Run**: min-time 100 ms/sample, warmup 1, samples 25, isolated=no, fast=no, pin-cpu=off, nice=False
- **Hash seed**: unset (isolated workers use 0 except the collision case)
- **GC**: disabled during the timed loop; collected before each sample
- **Threading**: single-threaded (including moka-py)
- **Libraries**:
  - cachebox: 6.2.9
  - cachetools: 7.2.7
  - cacheing: 0.1.1
  - lru-dict: 1.4.1
  - moka-py: 0.5.0
  - matplotlib: 3.11.2
  - matplotx: 0.3.10

## 📊 Set new (no eviction)

Insert keys that do not exist and do not trigger eviction. Cache is pre-filled to 25% of maxsize.

![set_new](photos/set_new.png)

- **Range**: 15.7× between fastest and slowest (median)
- **Best**: dict (66 ns, 14.9M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev |  MAD | Ops/sec | Samples |    CV |
| :------------------: | ----------: | --------: | ----: | ---: | ------: | ------: | ----: |
|         dict         |        66.0 |      67.2 |   3.4 |  0.3 |   14.9M |      25 |  5.1% |
|    cachebox.Cache    |       100.1 |     103.8 |  12.9 |  1.8 |    9.6M |     200 | 12.4% |
|   cachebox.RRCache   |       108.0 |     107.9 |   2.9 |  1.8 |    9.3M |     200 |  2.7% |
|  cachebox.FIFOCache  |       114.8 |     119.6 |  14.8 |  2.4 |    8.4M |     200 | 12.4% |
|  cachebox.LFUCache   |       140.1 |     140.7 |   3.1 |  2.2 |    7.1M |     200 |  2.2% |
|  cachebox.LRUCache   |       140.1 |     145.6 |  22.2 |  2.6 |    6.9M |     200 | 15.2% |
|       lru.LRU        |       160.7 |     161.2 |   4.0 |  2.8 |    6.2M |     200 |  2.5% |
|  cachebox.TTLCache   |       160.7 |     160.6 |   2.6 |  1.3 |    6.2M |     200 |  1.6% |
|  cachebox.VTTLCache  |       171.4 |     175.2 |  21.4 |  2.3 |    5.7M |     200 | 12.2% |
|   cachetools.Cache   |       208.5 |     218.7 |  26.9 |  9.1 |    4.6M |     200 | 12.3% |
| cacheing.RandomCache |       296.6 |     298.4 |   7.2 |  3.6 |    3.4M |     200 |  2.4% |
| cachetools.FIFOCache |       308.4 |     309.6 |   7.7 |  5.1 |    3.2M |     200 |  2.5% |
| cachetools.LFUCache  |       308.5 |     309.7 |   8.1 |  5.2 |    3.2M |     200 |  2.6% |
|  cachetools.RRCache  |       315.2 |     316.2 |   5.9 |  4.0 |    3.2M |     200 |  1.9% |
|  cacheing.LRUCache   |       335.4 |     336.6 |   5.7 |  4.2 |    3.0M |     200 |  1.7% |
|  cacheing.LFUCache   |       336.5 |     338.5 |   8.9 |  4.7 |    3.0M |     200 |  2.6% |
|     moka_py.Moka     |       403.4 |     403.8 |   6.2 |  4.6 |    2.5M |     200 |  1.5% |
|  moka_py.Moka (lru)  |       419.4 |     421.1 |  10.5 |  2.6 |    2.4M |     200 |  2.5% |
| cachetools.LRUCache  |       509.3 |     510.8 |  12.2 |  6.2 |    2.0M |     200 |  2.4% |
| cachetools.TTLCache  |       759.5 |     775.3 |  65.9 |  7.8 |    1.3M |     200 |  8.5% |
|  cacheing.TTLCache   |     1,039.0 |   1,059.4 | 111.6 | 40.1 |    0.9M |     200 | 10.5% |

## 📊 Set at capacity (eviction)

Insert new keys into a cache already at maxsize so each set evicts an entry.

![set_evict](photos/set_evict.png)

- **Range**: 16.3× between fastest and slowest (median)
- **Best**: cachebox.LRUCache (109 ns, 9.0M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev |  MAD | Ops/sec | Samples |    CV |
| :------------------: | ----------: | --------: | ----: | ---: | ------: | ------: | ----: |
|  cachebox.LRUCache   |       109.4 |     110.7 |   7.5 |  2.5 |    9.0M |     200 |  6.7% |
|  cachebox.FIFOCache  |       120.5 |     121.1 |   9.6 |  2.2 |    8.3M |     200 |  7.9% |
|   cachebox.RRCache   |       139.2 |     140.3 |   7.4 |  2.3 |    7.1M |     200 |  5.3% |
|  cachebox.TTLCache   |       175.0 |     175.4 |   7.9 |  4.0 |    5.7M |     200 |  4.5% |
|       lru.LRU        |       190.1 |     192.5 |  12.2 |  4.3 |    5.2M |     200 |  6.3% |
|  cachebox.LFUCache   |       204.8 |     206.6 |  12.4 |  4.8 |    4.8M |     200 |  6.0% |
|  cachebox.VTTLCache  |       247.4 |     250.3 |  17.0 |  5.5 |    4.0M |     200 |  6.8% |
|  cacheing.LRUCache   |       598.3 |     617.5 |  64.9 |  6.0 |    1.6M |     200 | 10.5% |
|     moka_py.Moka     |       678.2 |     695.1 |  59.3 |  7.2 |    1.4M |     149 |  8.5% |
| cachetools.FIFOCache |       689.5 |     711.1 |  69.1 |  8.4 |    1.4M |     200 |  9.7% |
|  cacheing.LFUCache   |       741.0 |     761.5 |  72.4 |  6.4 |    1.3M |     200 |  9.5% |
|  moka_py.Moka (lru)  |       752.8 |     766.6 |  63.1 | 11.9 |    1.3M |     200 |  8.2% |
| cachetools.LRUCache  |       928.9 |     933.4 |  60.1 | 46.9 |    1.1M |     192 |  6.4% |
|  cachetools.RRCache  |     1,013.6 |   1,030.7 |  54.3 |  9.6 |    1.0M |     135 |  5.3% |
| cacheing.RandomCache |     1,027.1 |   1,044.3 |  39.9 |  9.6 |    1.0M |     166 |  3.8% |
|  cacheing.TTLCache   |     1,403.9 |   1,436.6 | 109.7 | 34.9 |    0.7M |     126 |  7.6% |
| cachetools.LFUCache  |     1,773.0 |   1,783.7 |  28.7 |  5.6 |    0.6M |     200 |  1.6% |
| cachetools.TTLCache  |     1,781.6 |   1,799.0 |  70.4 | 11.3 |    0.6M |     125 |  3.9% |

Skipped: `dict` (no eviction policy), `cachebox.Cache` (no eviction policy), `cachetools.Cache` (no eviction policy)

## 📊 Lookup existing

Look up keys that are in the cache. LRU/LFU recency or frequency updates are part of the API cost.

![get_hit](photos/get_hit.png)

- **Range**: 13.2× between fastest and slowest (median)
- **Best**: dict (81 ns, 12.2M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev | MAD | Ops/sec | Samples |   CV |
| :------------------: | ----------: | --------: | ----: | --: | ------: | ------: | ---: |
|         dict         |        80.9 |      82.3 |   4.9 | 0.3 |   12.2M |      25 | 5.9% |
|    cachebox.Cache    |        90.4 |      90.4 |   0.7 | 0.6 |   11.1M |      25 | 0.8% |
|   cachebox.RRCache   |        90.8 |      90.8 |   0.3 | 0.3 |   11.0M |      25 | 0.4% |
|  cachebox.FIFOCache  |        92.9 |      93.0 |   0.3 | 0.2 |   10.7M |      25 | 0.3% |
|  cachebox.LFUCache   |        94.8 |      94.8 |   0.5 | 0.3 |   10.6M |      25 | 0.5% |
|  cachebox.LRUCache   |        96.4 |      96.4 |   0.5 | 0.3 |   10.4M |      25 | 0.5% |
| cacheing.RandomCache |       108.4 |     108.4 |   0.5 | 0.5 |    9.2M |      25 | 0.5% |
|  cachebox.VTTLCache  |       124.4 |     124.5 |   0.5 | 0.3 |    8.0M |      25 | 0.4% |
|  cachebox.TTLCache   |       126.8 |     126.6 |   0.9 | 0.8 |    7.9M |      25 | 0.7% |
|       lru.LRU        |       135.5 |     135.5 |   0.6 | 0.4 |    7.4M |      25 | 0.4% |
| cachetools.FIFOCache |       171.4 |     171.4 |   0.5 | 0.3 |    5.8M |      25 | 0.3% |
|  cachetools.RRCache  |       171.5 |     171.6 |   0.7 | 0.3 |    5.8M |      25 | 0.4% |
|   cachetools.Cache   |       172.2 |     172.2 |   0.6 | 0.5 |    5.8M |      25 | 0.3% |
|  cacheing.LRUCache   |       198.1 |     198.8 |   1.7 | 0.5 |    5.0M |      25 | 0.9% |
|  moka_py.Moka (lru)  |       231.2 |     232.0 |   4.9 | 0.9 |    4.3M |      25 | 2.1% |
|     moka_py.Moka     |       241.6 |     241.6 |   0.7 | 0.4 |    4.1M |      25 | 0.3% |
| cachetools.LRUCache  |       283.0 |     275.0 |  11.2 | 1.3 |    3.6M |      25 | 4.1% |
|  cacheing.LFUCache   |       364.6 |     361.8 |   5.7 | 1.9 |    2.8M |      25 | 1.6% |
| cachetools.LFUCache  |       411.9 |     414.2 |   9.1 | 0.6 |    2.4M |      25 | 2.2% |
|  cacheing.TTLCache   |       775.8 |     775.6 |   1.0 | 0.9 |    1.3M |      25 | 0.1% |
| cachetools.TTLCache  |     1,065.2 |   1,067.0 |   9.5 | 3.3 |    0.9M |      25 | 0.9% |

## 📊 Lookup missing

Look up keys that are not in a populated cache (mapping.get with default None).

![get_miss](photos/get_miss.png)

- **Range**: 19.5× between fastest and slowest (median)
- **Best**: dict (82 ns, 12.2M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev |  MAD | Ops/sec | Samples |   CV |
| :------------------: | ----------: | --------: | ----: | ---: | ------: | ------: | ---: |
|         dict         |        81.7 |      81.7 |   0.4 |  0.3 |   12.2M |      25 | 0.5% |
|  cachebox.LRUCache   |        91.0 |      90.9 |   0.5 |  0.3 |   11.0M |      25 | 0.6% |
|  cachebox.LFUCache   |        91.0 |      91.1 |   0.4 |  0.3 |   11.0M |      25 | 0.5% |
|   cachebox.RRCache   |        92.5 |      92.5 |   0.4 |  0.3 |   10.8M |      25 | 0.4% |
|  cachebox.FIFOCache  |        92.6 |      92.7 |   0.5 |  0.2 |   10.8M |      25 | 0.5% |
|    cachebox.Cache    |        92.8 |      92.7 |   0.4 |  0.3 |   10.8M |      25 | 0.4% |
|  cachebox.VTTLCache  |       104.8 |     105.0 |   1.2 |  1.1 |    9.5M |      25 | 1.2% |
|  cachebox.TTLCache   |       108.1 |     108.1 |   0.6 |  0.2 |    9.3M |      25 | 0.5% |
| cachetools.FIFOCache |       132.4 |     132.4 |   0.5 |  0.3 |    7.6M |      25 | 0.4% |
| cachetools.LFUCache  |       132.5 |     132.6 |   0.6 |  0.4 |    7.5M |      25 | 0.5% |
|   cachetools.Cache   |       132.7 |     132.7 |   0.4 |  0.3 |    7.5M |      25 | 0.3% |
| cachetools.LRUCache  |       132.8 |     132.9 |   0.8 |  0.4 |    7.5M |      25 | 0.6% |
|  cachetools.RRCache  |       133.0 |     133.1 |   0.5 |  0.2 |    7.5M |      25 | 0.4% |
|  moka_py.Moka (lru)  |       169.3 |     169.3 |   0.4 |  0.3 |    5.9M |      25 | 0.3% |
|     moka_py.Moka     |       179.4 |     179.8 |   2.4 |  1.4 |    5.6M |      25 | 1.3% |
|       lru.LRU        |       194.0 |     194.7 |   1.8 |  0.7 |    5.1M |      25 | 0.9% |
| cacheing.RandomCache |       464.7 |     468.9 |  10.0 |  2.5 |    2.1M |      25 | 2.1% |
|  cacheing.LFUCache   |       558.9 |     559.9 |   4.2 |  2.9 |    1.8M |      25 | 0.7% |
| cachetools.TTLCache  |       648.1 |     658.8 |  21.1 |  2.4 |    1.5M |      25 | 3.2% |
|  cacheing.LRUCache   |       687.8 |     691.2 |   6.2 |  1.0 |    1.4M |      25 | 0.9% |
|  cacheing.TTLCache   |     1,590.0 |   1,611.0 |  38.7 | 18.4 |    0.6M |      25 | 2.4% |

## 📊 Deletion

Delete keys that exist. Each sample populates maxsize entries and deletes them once.

![delete](photos/delete.png)

- **Range**: 9.4× between fastest and slowest (median)
- **Best**: dict (71 ns, 14.0M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev | MAD | Ops/sec | Samples |    CV |
| :------------------: | ----------: | --------: | ----: | --: | ------: | ------: | ----: |
|         dict         |        71.2 |      71.2 |   1.5 | 1.1 |   14.0M |     200 |  2.2% |
|    cachebox.Cache    |        92.8 |      93.8 |   9.8 | 2.0 |   10.7M |     200 | 10.4% |
|   cachebox.RRCache   |        93.8 |      94.1 |   2.5 | 1.8 |   10.6M |     200 |  2.7% |
|  cachebox.FIFOCache  |        94.1 |      94.0 |   2.4 | 1.7 |   10.6M |     200 |  2.5% |
|  cachebox.LRUCache   |       104.3 |     104.1 |   3.0 | 2.2 |    9.6M |     200 |  2.9% |
|       lru.LRU        |       108.0 |     108.4 |   3.1 | 2.3 |    9.2M |     200 |  2.8% |
|  cachebox.TTLCache   |       121.4 |     121.5 |   2.5 | 1.8 |    8.2M |     200 |  2.1% |
|   cachetools.Cache   |       145.9 |     146.3 |   3.6 | 2.9 |    6.8M |     200 |  2.5% |
|  cachebox.LFUCache   |       166.7 |     167.3 |   4.2 | 2.8 |    6.0M |     200 |  2.5% |
|  cachebox.VTTLCache  |       198.4 |     198.3 |   5.8 | 4.0 |    5.0M |     200 |  2.9% |
|  cacheing.LRUCache   |       227.1 |     227.6 |   5.9 | 4.9 |    4.4M |     200 |  2.6% |
| cachetools.FIFOCache |       236.1 |     236.7 |   5.6 | 4.6 |    4.2M |     200 |  2.4% |
| cachetools.LRUCache  |       238.6 |     238.7 |   6.2 | 5.5 |    4.2M |     200 |  2.6% |
| cachetools.LFUCache  |       270.3 |     270.4 |   5.9 | 5.0 |    3.7M |     200 |  2.2% |
|  cacheing.LFUCache   |       313.1 |     314.5 |   6.5 | 4.8 |    3.2M |     200 |  2.1% |
|  cachetools.RRCache  |       326.3 |     327.4 |   5.9 | 4.5 |    3.1M |     200 |  1.8% |
| cacheing.RandomCache |       346.6 |     346.5 |   6.0 | 4.3 |    2.9M |     199 |  1.7% |
| cachetools.TTLCache  |       538.4 |     539.3 |   4.8 | 2.7 |    1.9M |     200 |  0.9% |
|  cacheing.TTLCache   |       588.0 |     611.6 |  45.1 | 6.7 |    1.6M |     200 |  7.4% |
|     moka_py.Moka     |       665.3 |     665.9 |   6.5 | 4.2 |    1.5M |     110 |  1.0% |
|  moka_py.Moka (lru)  |       665.8 |     666.0 |   5.9 | 4.0 |    1.5M |     130 |  0.9% |

## 📊 Popitem

Call popitem() on a cache filled to maxsize (the eviction primitive).

![popitem](photos/popitem.png)

- **Range**: 14.0× between fastest and slowest (median)
- **Best**: cachebox.FIFOCache (95 ns, 10.5M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev | MAD | Ops/sec | Samples |   CV |
| :------------------: | ----------: | --------: | ----: | --: | ------: | ------: | ---: |
|  cachebox.FIFOCache  |        94.9 |      94.9 |   2.8 | 2.2 |   10.5M |     200 | 3.0% |
|  cachebox.LRUCache   |       105.3 |     105.4 |   2.3 | 1.6 |    9.5M |     200 | 2.2% |
|  cachebox.TTLCache   |       107.8 |     107.6 |   2.8 | 2.0 |    9.3M |     200 | 2.6% |
|       lru.LRU        |       137.6 |     137.9 |   4.4 | 2.5 |    7.3M |     200 | 3.2% |
|   cachebox.RRCache   |       147.0 |     147.4 |   5.7 | 3.2 |    6.8M |     200 | 3.9% |
|  cachebox.LFUCache   |       171.6 |     172.1 |   5.0 | 3.4 |    5.8M |     200 | 2.9% |
|  cachebox.VTTLCache  |       189.6 |     190.4 |   5.1 | 3.8 |    5.3M |     200 | 2.7% |
|  cacheing.LRUCache   |       241.5 |     242.5 |   6.2 | 5.0 |    4.1M |     200 | 2.6% |
|  cacheing.TTLCache   |       350.0 |     350.3 |   4.0 | 2.7 |    2.9M |     200 | 1.1% |
|  cacheing.LFUCache   |       357.8 |     358.6 |   6.3 | 3.3 |    2.8M |     200 | 1.8% |
| cachetools.LRUCache  |       396.9 |     397.1 |   6.7 | 4.7 |    2.5M |     155 | 1.7% |
| cachetools.FIFOCache |       397.7 |     397.5 |  10.0 | 5.7 |    2.5M |     187 | 2.5% |
|  cachetools.RRCache  |       640.8 |     641.8 |   8.5 | 5.2 |    1.6M |     200 | 1.3% |
| cacheing.RandomCache |       647.6 |     649.5 |  11.7 | 4.6 |    1.5M |     200 | 1.8% |
| cachetools.TTLCache  |       931.7 |     940.5 |  26.7 | 9.1 |    1.1M |     180 | 2.8% |
| cachetools.LFUCache  |     1,331.1 |   1,333.4 |  32.0 | 3.3 |    0.7M |     200 | 2.4% |

Skipped: `dict` (no eviction policy), `cachebox.Cache` (no eviction policy), `cachetools.Cache` (no eviction policy), `moka_py.Moka` (no popitem), `moka_py.Moka (lru)` (no popitem)

## 📊 Hash collision

Look up keys that all hash to the same value (hash() == 42).

![collision](photos/collision.png)

- **Range**: 7.4× between fastest and slowest (median)
- **Best**: cachebox.Cache (993 ns, 1.0M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev | MAD | Ops/sec | Samples |   CV |
| :------------------: | ----------: | --------: | ----: | --: | ------: | ------: | ---: |
|    cachebox.Cache    |       993.3 |     995.4 |   8.1 | 1.2 |    1.0M |      25 | 0.8% |
|   cachebox.RRCache   |       999.6 |   1,004.7 |  14.9 | 0.9 |    1.0M |      25 | 1.5% |
|  cachebox.LRUCache   |     1,037.4 |   1,036.9 |   2.1 | 1.1 |    1.0M |      25 | 0.2% |
|  cachebox.LFUCache   |     1,039.5 |   1,043.3 |  20.6 | 1.4 |    1.0M |      25 | 2.0% |
|  cachebox.VTTLCache  |     1,067.9 |   1,070.6 |  11.9 | 0.6 |    0.9M |      25 | 1.1% |
|         dict         |     1,169.9 |   1,169.9 |   0.8 | 0.6 |    0.9M |      25 | 0.1% |
|  cachebox.FIFOCache  |     1,182.0 |   1,182.4 |   1.6 | 0.3 |    0.8M |      25 | 0.1% |
| cacheing.RandomCache |     1,209.5 |   1,210.1 |   3.7 | 0.4 |    0.8M |      25 | 0.3% |
|  cachebox.TTLCache   |     1,211.4 |   1,213.6 |   5.2 | 0.7 |    0.8M |      25 | 0.4% |
|       lru.LRU        |     1,236.1 |   1,236.6 |   5.4 | 0.9 |    0.8M |      25 | 0.4% |
|     moka_py.Moka     |     2,115.0 |   2,115.0 |   4.1 | 2.4 |    0.5M |      25 | 0.2% |
|  moka_py.Moka (lru)  |     2,117.1 |   2,117.5 |   3.9 | 3.1 |    0.5M |      25 | 0.2% |
| cachetools.FIFOCache |     2,359.5 |   2,360.2 |   5.3 | 1.1 |    0.4M |      25 | 0.2% |
|   cachetools.Cache   |     2,359.9 |   2,359.8 |   1.9 | 1.6 |    0.4M |      25 | 0.1% |
|  cachetools.RRCache  |     2,374.4 |   2,374.3 |   1.3 | 0.7 |    0.4M |      25 | 0.1% |
|  cacheing.LRUCache   |     2,389.0 |   2,389.0 |   1.8 | 1.4 |    0.4M |      25 | 0.1% |
|  cacheing.TTLCache   |     3,010.2 |   3,011.0 |   2.2 | 1.1 |    0.3M |      25 | 0.1% |
| cachetools.LRUCache  |     3,564.4 |   3,566.7 |  15.5 | 2.3 |    0.3M |      25 | 0.4% |
| cachetools.TTLCache  |     5,548.5 |   5,553.4 |  17.8 | 3.9 |    0.2M |      25 | 0.3% |
|  cacheing.LFUCache   |     6,723.3 |   6,726.7 |  13.9 | 3.4 |    0.1M |      25 | 0.2% |
| cachetools.LFUCache  |     7,325.2 |   7,325.6 |  14.1 | 3.4 |    0.1M |      25 | 0.2% |

## 🚀 Usage

### Prerequisites

```bash
uv sync
```

### Run Benchmarks

```bash
# All cases (in-process)
python -m cachebox_benchmark

# One or more cases
python -m cachebox_benchmark get_hit delete

# Faster iteration (not for published numbers)
python -m cachebox_benchmark --fast

# One subprocess per (case, implementation)
python -m cachebox_benchmark --isolated

# JSON + regenerate README from a previous run
python -m cachebox_benchmark --json results.json
python -m cachebox_benchmark --report-only results.json
```

Optional host knobs (off by default): `--pin-cpu 0`, `--nice`.

### Understanding Results

- **Median (ns)**: robust typical cost per operation; tables are sorted by this.
- **Mean / Stdev / MAD**: distribution; MAD is median absolute deviation.
- **Ops/sec**: throughput from the mean.
- **CV**: stdev / mean. High CV means the number is noisy, not that the library is “bad”.
