# Caching libraries Benchmarks

According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...

If you know other library, tell me to add it to this page.

{{FAST_BANNER}}

> [!NOTE]\
> The `cacheing.VTTLCache` class was excluded from the benchmark because assigning a key raises `TypeError`.

## Methodology

Times are **from Python**: each sample is a calibrated inner loop around a single API call (`set` / `get` / `delete` / `popitem`, or one entry of an `items()` iteration). Setup and teardown are not timed. GC is collected before each sample and disabled during the timed region.

Reported values are the **median** ns/op (tables ranked by median), plus mean, stdev, MAD, ops/sec, sample count, and coefficient of variation. Outliers are **not** dropped. A result is flagged when CV > 10% or max > 1.5× mean.

All implementations use the same working set (`maxsize = 4096`, integer keys/values). TTL caches are constructed with a 3600s TTL so nothing expires during a sample. `dict`, `cachebox.Cache`, and `cachetools.Cache` have no eviction policy and are skipped on eviction cases.

| Case | What is measured |
| --- | --- |
| Set new (no eviction) | Insert keys that are not present and do not evict (cache ~25% full). |
| Set at capacity (eviction) | Insert new keys into a cache already at maxsize. |
| Lookup existing | `get` of a present key (LRU/LFU recency/frequency updates included). |
| Lookup missing | `get` of a missing key. |
| Deletion | Delete present keys (one delete per populated key, then a new cache). |
| Popitem | `popitem()` on a cache filled to maxsize. |
| Hash collision | `get` of keys whose `hash()` is always 42. |
| Iterate items | `for k, v in cache.items()` over a cache filled to maxsize; time is per entry. |

moka-py is a concurrent Rust cache measured **single-threaded** like the others.

## 🖥️ System Information

{{SYSTEM_INFO}}

{{RESULTS}}

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
