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
- cachebox version: 2.0.1
- cachetools version: 5.3.3
- cacheing version: 0.1.1


### Cache 

| Operation\Class | cachebox.Cache | cachetools.Cache | Python dictionary |
| --------------- | -------------- | ---------------- | ----------------- |
| clear           | 2.55ms/0.1KB   | 7.12ms/0.8KB     | 2.21ms/0.1KB      |
| delete          | 2.00ms/0.1KB   | 3.37ms/0.1KB     | 2.61ms/0.1KB      |
| get             | 2.51ms/0.1KB   | 2.14ms/0.1KB     | 2.28ms/0.1KB      |
| insert          | 2.70ms/23.8KB  | 5.43ms/69.0KB    | 2.77ms/69.0KB     |
| pop             | 2.60ms/0.1KB   | 3.82ms/0.1KB     | 2.56ms/0.1KB      |
| popitem         | N/A            | 5.07ms/0.2KB     | 2.44ms/0.1KB      |
| setdefault      | 2.73ms/23.8KB  | 5.47ms/69.0KB    | 2.45ms/69.0KB     |
| update          | 1.37ms/69.2KB  | 4.25ms/116.6KB   | 0.66ms/97.6KB     |

- 🥇 `dict` (Python dictionary) and `cachebox.Cache` are very similar (test with zero maxsize, you will see this)
- 🥈 `cachetools.Cache`

### FIFOCache 

| Operation\Class | cachebox.FIFOCache | cachetools.FIFOCache |
| --------------- | ------------------ | -------------------- |
| clear           | 29.21ms/0.1KB      | 48.55ms/0.9KB        |
| delete          | 2.73ms/0.1KB       | 3.31ms/0.1KB         |
| get             | 2.66ms/0.1KB       | 2.16ms/0.1KB         |
| insert          | 13.61ms/32.1KB     | 46.69ms/318.4KB      |
| pop             | 2.47ms/0.1KB       | 3.74ms/0.1KB         |
| popitem         | 2.36ms/0.1KB       | 5.77ms/0.2KB         |
| setdefault      | 9.12ms/32.1KB      | 55.26ms/318.4KB      |
| update          | 4.06ms/609.2KB     | 52.54ms/893.1KB      |

- 🥇 `cachebox.FIFOCache`
- 🥈 `cachetools.FIFOCache`

### LFUCache 

| Operation\Class | cachebox.LFUCache | cachetools.LFUCache | cacheing.LFUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.15ms/0.1KB      | 125.74ms/1.0KB      | 33.78ms/0.9KB     |
| delete          | 2.95ms/0.1KB      | 2.26ms/0.2KB        | 3.50ms/0.1KB      |
| get             | 2.58ms/0.1KB      | 3.27ms/0.1KB        | 4.04ms/109.3KB    |
| insert          | 29.20ms/27.8KB    | 500.33ms/253.3KB    | 29.88ms/392.0KB   |
| pop             | 4.33ms/0.1KB      | 4.97ms/0.2KB        | 6.00ms/0.7KB      |
| popitem         | 6.16ms/0.1KB      | 42.98ms/0.4KB       | 4.36ms/0.1KB      |
| setdefault      | 36.43ms/28.1KB    | 560.49ms/253.3KB    | 62.81ms/393.0KB   |
| update          | 36.29ms/609.2KB   | 549.29ms/828.0KB    | 21.07ms/966.7KB   |

- 🥇 `cachebox.LFUCache`
- 🥈 `cacheing.LFUCache`
- 🥉 `cachetools.LFUCache`

### LRUCache 

| Operation\Class | cachebox.LRUCache | cachetools.LRUCache | cacheing.LRUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 17.17ms/0.1KB     | 40.85ms/0.9KB       | 32.88ms/0.9KB     |
| delete          | 2.87ms/0.1KB      | 3.74ms/0.1KB        | 3.10ms/0.1KB      |
| get             | 2.65ms/0.1KB      | 2.99ms/0.1KB        | 2.98ms/0.1KB      |
| insert          | 13.83ms/32.1KB    | 48.88ms/318.4KB     | 33.60ms/318.0KB   |
| pop             | 2.52ms/0.1KB      | 3.75ms/0.1KB        | 4.65ms/0.1KB      |
| popitem         | 2.60ms/0.1KB      | 3.95ms/0.2KB        | 5.52ms/0.1KB      |
| setdefault      | 12.65ms/32.1KB    | 47.41ms/318.4KB     | 87.97ms/319.2KB   |
| update          | 7.13ms/609.2KB    | 53.17ms/893.1KB     | 19.30ms/892.8KB   |

- 🥇 `cachebox.LRUCache`
- 🥈 `cacheing.LRUCache`
- 🥉 `cachetools.LRUCache`

### RRCache 

| Operation\Class | cachebox.RRCache | cachetools.RRCache | cacheing.RandomCache |
| --------------- | ---------------- | ------------------ | -------------------- |
| clear           | 10.73ms/0.1KB    | 75.34ms/8.3KB      | 57.18ms/5.2KB        |
| delete          | 5.43ms/0.1KB     | 3.12ms/0.1KB       | 1.90ms/5.1KB         |
| get             | 3.39ms/0.1KB     | 2.59ms/0.1KB       | 1.95ms/0.1KB         |
| insert          | 27.59ms/32.0KB   | 105.11ms/179.6KB   | 54.05ms/285.9KB      |
| pop             | 2.42ms/0.1KB     | 3.74ms/0.1KB       | 5.98ms/5.1KB         |
| popitem         | 3.53ms/0.1KB     | 14.22ms/8.3KB      | 9.75ms/5.2KB         |
| setdefault      | 17.14ms/32.1KB   | 111.84ms/179.6KB   | 68.01ms/286.6KB      |
| update          | 17.58ms/609.2KB  | 132.18ms/754.3KB   | 40.80ms/860.6KB      |

- 🥇 `cachebox.RRCache`
- 🥈 `cacheing.RandomCache`
- 🥉 `cachetools.RRCache`

### TTLCache 

| Operation\Class | cachebox.TTLCache | cachetools.TTLCache | cacheing.TTLCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 21.28ms/0.1KB     | 69.25ms/1.0KB       | 41.00ms/1.1KB     |
| delete          | 2.36ms/0.1KB      | 5.05ms/0.2KB        | 2.54ms/0.2KB      |
| get             | 2.37ms/0.1KB      | 1.30ms/0.2KB        | 7.31ms/0.2KB      |
| insert          | 22.24ms/32.1KB    | 124.60ms/406.7KB    | 78.54ms/1878.3KB  |
| pop             | 1.81ms/0.1KB      | 7.80ms/0.3KB        | 3.85ms/0.2KB      |
| popitem         | 2.76ms/0.1KB      | 5.39ms/0.4KB        | 1.55ms/0.1KB      |
| setdefault      | 23.89ms/32.1KB    | 155.65ms/404.5KB    | 146.26ms/1877.9KB |
| update          | 10.71ms/609.2KB   | 114.78ms/981.4KB    | 57.24ms/2173.3KB  |

- 🥇 `cachebox.TTLCache`
- 🥈 `cacheing.TTLCache`
- 🥉 `cachetools.TTLCache`

### VTTLCache 

| Operation\Class | cachebox.VTTLCache | cacheing.VTTLCache |
| --------------- | ------------------ | ------------------ |
| clear           | 8.23ms/0.1KB       | 38.31ms/1.1KB      |
| delete          | 3.34ms/0.1KB       | 2.02ms/0.2KB       |
| get             | 2.73ms/0.1KB       | 1.66ms/0.2KB       |
| insert          | 123.41ms/32.1KB    | 12808.14ms/1884.7KB |
| pop             | 3.31ms/0.1KB       | 3.23ms/0.2KB       |
| popitem         | 2.55ms/0.1KB       | 1.25ms/0.1KB       |
| setdefault      | 122.71ms/32.1KB    | 12870.23ms/1886.5KB |
| update          | 7.00ms/609.2KB     | 12905.77ms/2631.1KB |

- 🥇 `cachebox.VTTLCache`
- 🥈 `cacheing.VTTLCache`

> [!TIP]\
> According to this benchmark, In `cachebox.VTTLCache` if you want to insert several values in a time, use `update` instead of `insert` or `__setitem__`.

## Run yourself
1. Download source from here.
```sh
git clone https://github.com/awolverp/cachebox-benchmark
cd cachebox-benchmark
```

2. Install/Upgrade requirements:
```sh
pip3 install -U -r requirements.txt
```

3. You can run benchmark using `make` script or manually:
```sh
# Make:
make

# Manually:
python3 main.py Cache FIFOCache LFUCache LRUCache RRCache TTLCache VTTLCache
```
