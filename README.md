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

- **Platform**: Linux-7.2.3-arch1-2-x86_64-with-glibc2.44
- **Python**: 3.14.7
- **Processor**: 11th Gen Intel(R) Core(TM) i3-1115G4 @ 3.00GHz
- **Timer**: resolution 652.0 ns, overhead 42.0 ns
- **Run**: min-time 100 ms/sample, warmup 1, samples 25, isolated=no, fast=no, pin-cpu=off, nice=False
- **Hash seed**: unset (isolated workers use 0 except the collision case)
- **GC**: disabled during the timed loop; collected before each sample
- **Threading**: single-threaded (including moka-py)
- **Libraries**:
  - cachebox: 6.2.7
  - cachetools: 7.1.8
  - cacheing: 0.1.1
  - lru-dict: 1.4.1
  - moka-py: 0.5.0

## 📊 Set new (no eviction)

Insert keys that do not exist and do not trigger eviction. Cache is pre-filled to 25% of maxsize.

![set_new](photos/set_new.png)

- **Range**: 42.9× between fastest and slowest (median)
- **Best**: dict (70 ns, 14.1M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev | MAD | Ops/sec | Samples |    CV |
| :------------------: | ----------: | --------: | ----: | --: | ------: | ------: | ----: |
|         dict         |        69.6 |      71.1 |   4.2 | 0.5 |   14.1M |      25 |  5.8% |
|    cachebox.Cache    |        86.7 |      87.4 |   4.0 | 0.9 |   11.4M |     200 |  4.5% |
|   cachebox.RRCache   |        93.2 |      94.3 |   8.4 | 0.9 |   10.6M |     200 |  8.9% |
|  cachebox.FIFOCache  |        94.0 |      95.1 |   7.8 | 0.9 |   10.5M |     200 |  8.2% |
|  cachebox.LRUCache   |       126.6 |     127.2 |   2.6 | 1.4 |    7.9M |     200 |  2.0% |
|  cachebox.LFUCache   |       128.4 |     129.2 |   3.7 | 1.2 |    7.7M |     200 |  2.9% |
|  cachebox.TTLCache   |       139.8 |     140.2 |   2.1 | 1.1 |    7.1M |     200 |  1.5% |
|       lru.LRU        |       157.7 |     158.8 |   8.8 | 1.3 |    6.3M |     200 |  5.5% |
| cacheing.RandomCache |       285.1 |     290.4 |  33.9 | 1.7 |    3.4M |     200 | 11.7% |
|   cachetools.Cache   |       293.4 |     297.5 |  14.8 | 1.8 |    3.4M |     200 |  5.0% |
|  cacheing.LRUCache   |       322.0 |     323.0 |   4.6 | 1.5 |    3.1M |     200 |  1.4% |
|  cacheing.LFUCache   |       324.7 |     328.8 |  15.8 | 1.9 |    3.0M |     200 |  4.8% |
|     moka_py.Moka     |       396.5 |     397.9 |  12.0 | 2.2 |    2.5M |     200 |  3.0% |
| cachetools.LFUCache  |       400.4 |     402.5 |   6.6 | 1.7 |    2.5M |     200 |  1.6% |
|  moka_py.Moka (lru)  |       403.4 |     405.1 |  10.0 | 2.2 |    2.5M |     200 |  2.5% |
| cachetools.FIFOCache |       407.6 |     409.1 |  11.4 | 2.3 |    2.4M |     200 |  2.8% |
|  cachetools.RRCache  |       412.6 |     420.7 |  29.6 | 2.6 |    2.4M |     200 |  7.0% |
| cachetools.LRUCache  |       606.0 |     617.2 |  24.4 | 5.6 |    1.6M |     200 |  4.0% |
|  cacheing.TTLCache   |       988.8 |     994.6 |  21.6 | 7.4 |    1.0M |     200 |  2.2% |
| cachetools.TTLCache  |     1,118.8 |   1,129.9 |  83.7 | 5.1 |    0.9M |     200 |  7.4% |
|  cachebox.VTTLCache  |     2,987.5 |   3,020.8 | 298.7 | 2.7 |    0.3M |     200 |  9.9% |

## 📊 Set at capacity (eviction)

Insert new keys into a cache already at maxsize so each set evicts an entry.

![set_evict](photos/set_evict.png)

- **Range**: 49.7× between fastest and slowest (median)
- **Best**: cachebox.LRUCache (105 ns, 9.5M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev |  MAD | Ops/sec | Samples |    CV |
| :------------------: | ----------: | --------: | ----: | ---: | ------: | ------: | ----: |
|  cachebox.LRUCache   |       104.5 |     105.0 |   3.1 |  1.3 |    9.5M |     200 |  2.9% |
|  cachebox.FIFOCache  |       108.4 |     110.2 |  12.0 |  1.0 |    9.1M |     200 | 10.9% |
|  cachebox.TTLCache   |       152.1 |     152.9 |   5.7 |  1.0 |    6.5M |     200 |  3.7% |
|       lru.LRU        |       185.1 |     185.3 |   2.2 |  1.1 |    5.4M |     200 |  1.2% |
|  cacheing.LRUCache   |       572.2 |     579.7 |  22.3 |  3.7 |    1.7M |     200 |  3.8% |
|     moka_py.Moka     |       676.0 |     685.4 |  27.6 |  6.1 |    1.5M |     200 |  4.0% |
|  cacheing.LFUCache   |       732.7 |     739.6 |  22.7 |  7.6 |    1.4M |     200 |  3.1% |
|  moka_py.Moka (lru)  |       748.2 |     752.5 |  21.4 |  3.4 |    1.3M |     200 |  2.8% |
| cachetools.FIFOCache |       899.1 |     902.2 |  14.5 |  3.0 |    1.1M |     186 |  1.6% |
| cacheing.RandomCache |       993.2 |   1,010.2 |  69.7 |  6.7 |    1.0M |     167 |  6.9% |
|  cachetools.RRCache  |     1,209.7 |   1,224.0 |  46.1 | 27.2 |    0.8M |     136 |  3.8% |
|   cachebox.RRCache   |     1,243.3 |   1,321.6 | 299.4 |  8.4 |    0.8M |     200 | 22.7% |
| cachetools.LRUCache  |     1,258.7 |   1,285.2 |  74.5 |  9.0 |    0.8M |     140 |  5.8% |
|  cacheing.TTLCache   |     1,392.0 |   1,402.8 |  27.9 | 11.7 |    0.7M |     124 |  2.0% |
| cachetools.LFUCache  |     2,544.2 |   2,563.9 |  49.7 | 17.8 |    0.4M |     135 |  1.9% |
| cachetools.TTLCache  |     3,116.0 |   3,140.3 |  57.6 | 26.7 |    0.3M |      83 |  1.8% |
|  cachebox.LFUCache   |     4,024.0 |   3,977.8 |  98.4 | 97.1 |    0.3M |     100 |  2.5% |
|  cachebox.VTTLCache  |     5,193.4 |   5,140.3 | 149.8 | 93.6 |    0.2M |      86 |  2.9% |

Skipped: `dict` (no eviction policy), `cachebox.Cache` (no eviction policy), `cachetools.Cache` (no eviction policy)

## 📊 Lookup existing

Look up keys that are in the cache. LRU/LFU recency or frequency updates are part of the API cost.

![get_hit](photos/get_hit.png)

- **Range**: 12.4× between fastest and slowest (median)
- **Best**: dict (80 ns, 12.5M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev | MAD | Ops/sec | Samples |   CV |
| :------------------: | ----------: | --------: | ----: | --: | ------: | ------: | ---: |
|         dict         |        79.8 |      80.1 |   0.7 | 0.2 |   12.5M |      25 | 0.9% |
|   cachebox.RRCache   |        86.1 |      86.2 |   0.4 | 0.2 |   11.6M |      25 | 0.4% |
|    cachebox.Cache    |        87.2 |      87.2 |   0.3 | 0.2 |   11.5M |      25 | 0.4% |
|  cachebox.LFUCache   |        90.6 |      91.0 |   1.6 | 0.2 |   11.0M |      25 | 1.8% |
|  cachebox.FIFOCache  |        91.5 |      91.9 |   1.2 | 0.3 |   10.9M |      25 | 1.3% |
|  cachebox.LRUCache   |        93.7 |      94.0 |   1.3 | 0.6 |   10.6M |      25 | 1.4% |
| cacheing.RandomCache |       106.0 |     106.4 |   1.1 | 0.4 |    9.4M |      25 | 1.0% |
|  cachebox.VTTLCache  |       118.2 |     118.4 |   0.8 | 0.2 |    8.4M |      25 | 0.6% |
|  cachebox.TTLCache   |       123.3 |     123.8 |   1.9 | 0.4 |    8.1M |      25 | 1.5% |
|       lru.LRU        |       128.9 |     129.0 |   0.6 | 0.2 |    7.8M |      25 | 0.4% |
|   cachetools.Cache   |       168.9 |     169.3 |   1.4 | 0.4 |    5.9M |      25 | 0.8% |
|  cachetools.RRCache  |       169.0 |     169.3 |   1.0 | 0.4 |    5.9M |      25 | 0.6% |
| cachetools.FIFOCache |       169.4 |     170.1 |   2.2 | 0.3 |    5.9M |      25 | 1.3% |
|  cacheing.LRUCache   |       197.7 |     198.4 |   3.0 | 0.5 |    5.0M |      25 | 1.5% |
|  moka_py.Moka (lru)  |       231.8 |     233.5 |   5.2 | 0.2 |    4.3M |      25 | 2.2% |
|     moka_py.Moka     |       240.5 |     241.5 |   2.6 | 0.2 |    4.1M |      25 | 1.1% |
| cachetools.LRUCache  |       337.6 |     341.5 |   8.3 | 0.3 |    2.9M |      25 | 2.4% |
|  cacheing.LFUCache   |       365.1 |     364.7 |   6.6 | 3.2 |    2.7M |      25 | 1.8% |
| cachetools.LFUCache  |       444.0 |     446.3 |   4.3 | 1.3 |    2.2M |      25 | 1.0% |
|  cacheing.TTLCache   |       700.5 |     702.9 |   4.3 | 1.3 |    1.4M |      25 | 0.6% |
| cachetools.TTLCache  |       991.6 |     992.9 |   7.8 | 2.2 |    1.0M |      25 | 0.8% |

## 📊 Lookup missing

Look up keys that are not in a populated cache (mapping.get with default None).

![get_miss](photos/get_miss.png)

- **Range**: 20.7× between fastest and slowest (median)
- **Best**: dict (82 ns, 12.2M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev |  MAD | Ops/sec | Samples |   CV |
| :------------------: | ----------: | --------: | ----: | ---: | ------: | ------: | ---: |
|         dict         |        81.7 |      81.9 |   1.1 |  0.3 |   12.2M |      25 | 1.3% |
| cachetools.LFUCache  |       131.6 |     131.6 |   0.9 |  0.5 |    7.6M |      25 | 0.7% |
|  cachetools.RRCache  |       131.6 |     133.1 |   2.8 |  0.5 |    7.5M |      25 | 2.1% |
| cachetools.LRUCache  |       133.3 |     134.5 |   2.3 |  0.9 |    7.4M |      25 | 1.7% |
|   cachetools.Cache   |       133.6 |     134.8 |   2.2 |  1.1 |    7.4M |      25 | 1.6% |
| cachetools.FIFOCache |       135.1 |     135.2 |   2.1 |  0.4 |    7.4M |      25 | 1.6% |
|  moka_py.Moka (lru)  |       174.7 |     175.0 |   3.2 |  3.0 |    5.7M |      25 | 1.8% |
|     moka_py.Moka     |       186.5 |     185.6 |   4.2 |  3.2 |    5.4M |      25 | 2.3% |
|       lru.LRU        |       199.8 |     201.7 |   5.7 |  0.6 |    5.0M |      25 | 2.8% |
| cacheing.RandomCache |       493.3 |     495.3 |   9.7 |  3.6 |    2.0M |      25 | 2.0% |
|  cacheing.LFUCache   |       577.7 |     581.0 |  11.0 |  2.4 |    1.7M |      25 | 1.9% |
| cachetools.TTLCache  |       676.0 |     676.0 |  10.7 |  5.1 |    1.5M |      25 | 1.6% |
|  cacheing.LRUCache   |       697.7 |     700.8 |   8.8 |  0.6 |    1.4M |      25 | 1.2% |
|   cachebox.RRCache   |     1,082.5 |   1,088.8 |  16.5 |  6.4 |    0.9M |      25 | 1.5% |
|    cachebox.Cache    |     1,087.8 |   1,092.6 |  13.4 |  2.8 |    0.9M |      25 | 1.2% |
|  cachebox.VTTLCache  |     1,166.0 |   1,171.4 |  12.1 |  2.2 |    0.9M |      25 | 1.0% |
|  cachebox.LRUCache   |     1,175.5 |   1,180.6 |  10.8 |  4.8 |    0.8M |      25 | 0.9% |
|  cachebox.LFUCache   |     1,180.3 |   1,183.0 |   8.0 |  4.0 |    0.8M |      25 | 0.7% |
|  cachebox.TTLCache   |     1,332.6 |   1,339.2 |  15.8 |  3.8 |    0.7M |      25 | 1.2% |
|  cachebox.FIFOCache  |     1,349.4 |   1,354.0 |   9.6 |  3.5 |    0.7M |      25 | 0.7% |
|  cacheing.TTLCache   |     1,687.7 |   1,689.5 |  29.9 | 14.3 |    0.6M |      25 | 1.8% |

## 📊 Deletion

Delete keys that exist. Each sample populates maxsize entries and deletes them once.

![delete](photos/delete.png)

- **Range**: 9.7× between fastest and slowest (median)
- **Best**: dict (69 ns, 14.5M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev | MAD | Ops/sec | Samples |    CV |
| :------------------: | ----------: | --------: | ----: | --: | ------: | ------: | ----: |
|         dict         |        68.9 |      69.2 |   1.7 | 0.6 |   14.5M |     200 |  2.5% |
|    cachebox.Cache    |        73.7 |      74.4 |   6.4 | 0.8 |   13.4M |     200 |  8.6% |
|   cachebox.RRCache   |        74.7 |      76.0 |   8.0 | 0.9 |   13.2M |     200 | 10.6% |
|  cachebox.FIFOCache  |        83.2 |      83.4 |   1.5 | 0.7 |   12.0M |     200 |  1.8% |
|  cachebox.LRUCache   |        87.6 |      87.8 |   2.2 | 1.0 |   11.4M |     200 |  2.5% |
|  cachebox.LFUCache   |        97.2 |      98.5 |   9.9 | 0.8 |   10.2M |     200 | 10.1% |
|       lru.LRU        |       105.6 |     106.1 |   4.4 | 0.8 |    9.4M |     200 |  4.1% |
|  cachebox.TTLCache   |       107.4 |     107.7 |   1.9 | 0.8 |    9.3M |     200 |  1.8% |
|  cachebox.VTTLCache  |       117.8 |     118.6 |   3.8 | 1.0 |    8.4M |     156 |  3.2% |
|   cachetools.Cache   |       168.2 |     168.4 |   2.0 | 0.8 |    5.9M |     200 |  1.2% |
|  cacheing.LRUCache   |       217.8 |     220.6 |  20.2 | 0.9 |    4.5M |     200 |  9.2% |
| cachetools.FIFOCache |       260.3 |     262.3 |  12.0 | 0.9 |    3.8M |     200 |  4.6% |
| cachetools.LRUCache  |       260.5 |     261.2 |   5.7 | 0.8 |    3.8M |     200 |  2.2% |
| cachetools.LFUCache  |       290.4 |     292.3 |  12.0 | 0.9 |    3.4M |     200 |  4.1% |
|  cacheing.LFUCache   |       300.5 |     303.8 |  24.1 | 1.3 |    3.3M |     200 |  7.9% |
| cacheing.RandomCache |       331.8 |     338.5 |  16.7 | 1.7 |    3.0M |     200 |  4.9% |
|  cachetools.RRCache  |       344.7 |     346.3 |  11.8 | 1.3 |    2.9M |     200 |  3.4% |
| cachetools.TTLCache  |       559.6 |     561.3 |   7.5 | 1.4 |    1.8M |     200 |  1.3% |
|  cacheing.TTLCache   |       573.8 |     582.9 |  40.7 | 4.6 |    1.7M |     200 |  7.0% |
|  moka_py.Moka (lru)  |       662.7 |     664.7 |  10.0 | 2.0 |    1.5M |     121 |  1.5% |
|     moka_py.Moka     |       667.2 |     685.1 |  63.0 | 6.4 |    1.5M |     200 |  9.2% |

## 📊 Popitem

Call popitem() on a cache filled to maxsize (the eviction primitive).

![popitem](photos/popitem.png)

- **Range**: 23.5× between fastest and slowest (median)
- **Best**: cachebox.FIFOCache (85 ns, 11.7M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev |  MAD | Ops/sec | Samples |    CV |
| :------------------: | ----------: | --------: | ----: | ---: | ------: | ------: | ----: |
|  cachebox.FIFOCache  |        84.9 |      85.5 |   5.9 |  1.2 |   11.7M |     200 |  6.9% |
|  cachebox.TTLCache   |        94.9 |      95.9 |   8.2 |  1.2 |   10.4M |     200 |  8.5% |
|  cachebox.LRUCache   |        95.9 |      96.1 |   2.1 |  0.9 |   10.4M |     200 |  2.1% |
|  cachebox.LFUCache   |        97.4 |      99.3 |  12.0 |  1.2 |   10.1M |     200 | 12.1% |
|  cachebox.VTTLCache  |       108.9 |     110.9 |   9.4 |  1.4 |    9.0M |     176 |  8.5% |
|       lru.LRU        |       129.8 |     130.3 |   5.4 |  0.9 |    7.7M |     200 |  4.1% |
|  cacheing.LRUCache   |       230.0 |     230.9 |   7.4 |  1.2 |    4.3M |     200 |  3.2% |
|  cacheing.TTLCache   |       343.5 |     347.2 |  56.4 |  2.8 |    2.9M |     200 | 16.2% |
|  cacheing.LFUCache   |       348.6 |     351.0 |  14.0 |  1.9 |    2.8M |     200 |  4.0% |
| cachetools.FIFOCache |       493.7 |     497.1 |  15.0 |  1.9 |    2.0M |     200 |  3.0% |
| cacheing.RandomCache |       637.3 |     660.2 |  49.6 | 13.1 |    1.5M |     141 |  7.5% |
| cachetools.LRUCache  |       650.1 |     658.2 |  40.5 |  2.3 |    1.5M |     200 |  6.2% |
|   cachebox.RRCache   |       703.8 |     712.2 |  39.4 |  7.5 |    1.4M |     200 |  5.5% |
|  cachetools.RRCache  |       727.7 |     740.4 |  63.2 |  6.7 |    1.4M |     172 |  8.5% |
| cachetools.TTLCache  |     1,786.9 |   1,812.9 |  69.3 | 24.8 |    0.6M |     122 |  3.8% |
| cachetools.LFUCache  |     1,995.1 |   2,010.2 |  65.8 | 33.9 |    0.5M |     196 |  3.3% |

Skipped: `dict` (no eviction policy), `cachebox.Cache` (no eviction policy), `cachetools.Cache` (no eviction policy), `moka_py.Moka` (no popitem), `moka_py.Moka (lru)` (no popitem)

## 📊 Hash collision

Look up keys that all hash to the same value (hash() == 42).

![collision](photos/collision.png)

- **Range**: 6.9× between fastest and slowest (median)
- **Best**: cachebox.RRCache (1010 ns, 1.0M ops/sec)

|    Implementation    | Median (ns) | Mean (ns) | Stdev |  MAD | Ops/sec | Samples |   CV |
| :------------------: | ----------: | --------: | ----: | ---: | ------: | ------: | ---: |
|   cachebox.RRCache   |     1,009.8 |   1,018.3 |  17.3 |  8.1 |    1.0M |      25 | 1.7% |
|    cachebox.Cache    |     1,021.1 |   1,020.8 |  20.5 | 12.2 |    1.0M |      25 | 2.0% |
|  cachebox.LFUCache   |     1,048.9 |   1,056.2 |  16.7 | 10.7 |    0.9M |      25 | 1.6% |
|  cachebox.VTTLCache  |     1,068.9 |   1,063.3 |  18.2 | 10.0 |    0.9M |      25 | 1.7% |
|  cachebox.LRUCache   |     1,076.5 |   1,068.3 |  21.5 |  7.8 |    0.9M |      25 | 2.0% |
| cacheing.RandomCache |     1,179.2 |   1,184.9 |  15.0 |  0.7 |    0.8M |      25 | 1.3% |
|         dict         |     1,179.3 |   1,173.3 |  20.0 | 18.5 |    0.9M |      25 | 1.7% |
|  cachebox.FIFOCache  |     1,203.0 |   1,195.0 |  23.5 | 17.9 |    0.8M |      25 | 2.0% |
|  cachebox.TTLCache   |     1,217.7 |   1,216.1 |  17.8 | 18.2 |    0.8M |      25 | 1.5% |
|       lru.LRU        |     1,248.0 |   1,239.2 |  18.9 | 14.8 |    0.8M |      25 | 1.5% |
|     moka_py.Moka     |     2,040.4 |   2,042.3 |   6.9 |  2.0 |    0.5M |      25 | 0.3% |
|  moka_py.Moka (lru)  |     2,047.2 |   2,048.9 |   9.6 |  1.5 |    0.5M |      25 | 0.5% |
| cachetools.FIFOCache |     2,320.3 |   2,338.7 |  35.7 |  3.0 |    0.4M |      25 | 1.5% |
|  cachetools.RRCache  |     2,323.9 |   2,336.4 |  23.3 |  7.5 |    0.4M |      25 | 1.0% |
|   cachetools.Cache   |     2,324.7 |   2,335.8 |  25.5 |  5.4 |    0.4M |      25 | 1.1% |
|  cacheing.LRUCache   |     2,366.3 |   2,387.0 |  33.2 | 11.6 |    0.4M |      25 | 1.4% |
|  cacheing.TTLCache   |     2,928.7 |   2,921.8 |  44.2 | 42.2 |    0.3M |      25 | 1.5% |
| cachetools.LRUCache  |     4,698.1 |   4,730.9 |  57.3 | 14.1 |    0.2M |      25 | 1.2% |
|  cacheing.LFUCache   |     5,303.0 |   5,337.7 |  63.8 | 13.2 |    0.2M |      25 | 1.2% |
| cachetools.TTLCache  |     5,367.8 |   5,413.9 |  93.6 |  5.1 |    0.2M |      25 | 1.7% |
| cachetools.LFUCache  |     6,987.7 |   7,029.0 |  77.3 |  8.9 |    0.1M |      25 | 1.1% |

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
