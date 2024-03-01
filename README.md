# Caching libraries Benchmarks
According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries
I know, to show power of my library ...

**Qualification criteria is:**
- Needs to support minimum 2 alghoritms
- Runs on Python3.8+

If you know other library, tell me to add it to this page.

> [!IMPORTANT]\
> The system on which the benchmarks are done: **Linux x86_64, 8G, Intel i3-1115G4**

## Benchmarks:
**Versions**:
- cachebox version: 1.0.21
- cachetools version: 5.3.2
- cacheing version: 0.1.1


### Cache 

| Operation\Class | cachebox.Cache | cachetools.Cache |
| --------------- | -------------- | ---------------- |
| clear           | 1.23ms/0.1KB   | 4.52ms/0.8KB     |
| delete          | 1.05ms/0.1KB   | 0.92ms/0.1KB     |
| get             | 0.79ms/0.1KB   | 0.66ms/0.1KB     |
| insert          | 0.83ms/23.8KB  | 1.49ms/69.0KB    |
| pop             | 0.70ms/0.1KB   | 1.10ms/0.1KB     |
| popitem         | 0.00ms/0.0KB   | 1.66ms/0.2KB     |
| setdefault      | 0.72ms/23.8KB  | 1.78ms/69.0KB    |
| update          | 0.30ms/69.2KB  | 1.13ms/116.6KB   |

- 🥇 `cachebox.Cache`
- 🥈 `cachetools.Cache`

### FIFOCache 

| Operation\Class | cachebox.FIFOCache | cachetools.FIFOCache |
| --------------- | ------------------ | -------------------- |
| clear           | 8.39ms/0.1KB       | 40.60ms/0.9KB        |
| delete          | 0.79ms/0.1KB       | 1.04ms/0.1KB         |
| get             | 0.74ms/0.1KB       | 0.63ms/0.1KB         |
| insert          | 13.02ms/32.1KB     | 42.95ms/318.4KB      |
| pop             | 1.10ms/0.1KB       | 1.19ms/0.1KB         |
| popitem         | 0.74ms/0.1KB       | 1.52ms/0.2KB         |
| setdefault      | 9.99ms/32.1KB      | 44.43ms/318.4KB      |
| update          | 9.33ms/1135.1KB    | 40.51ms/893.1KB      |

- 🥇 `cachebox.FIFOCache`
- 🥈 `cachetools.FIFOCache`

### LFUCache 

| Operation\Class | cachebox.LFUCache | cachetools.LFUCache | cacheing.LFUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.92ms/0.1KB      | 122.70ms/1.0KB      | 32.32ms/0.9KB     |
| delete          | 0.81ms/0.1KB      | 1.61ms/0.2KB        | 1.16ms/0.1KB      |
| get             | 0.78ms/0.1KB      | 0.90ms/0.1KB        | 1.25ms/109.3KB    |
| insert          | 45.47ms/23.9KB    | 499.85ms/253.3KB    | 24.26ms/392.0KB   |
| pop             | 0.76ms/0.1KB      | 2.08ms/0.2KB        | 1.90ms/0.7KB      |
| popitem         | 3.79ms/0.1KB      | 29.03ms/0.4KB       | 1.29ms/0.1KB      |
| setdefault      | 42.88ms/23.9KB    | 513.87ms/253.3KB    | 51.69ms/393.0KB   |
| update          | 40.14ms/1135.1KB  | 520.63ms/828.0KB    | 18.22ms/966.7KB   |

- 🥇 `cacheing.LFUCache`
- 🥈 `cachebox.LFUCache`
- 🥉 `cachetools.LFUCache`

### LRUCache 

| Operation\Class | cachebox.LRUCache | cachetools.LRUCache | cacheing.LRUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.68ms/0.1KB      | 43.36ms/0.9KB       | 32.58ms/0.9KB     |
| delete          | 0.80ms/0.1KB      | 1.02ms/0.1KB        | 0.99ms/0.1KB      |
| get             | 0.76ms/0.1KB      | 0.79ms/0.1KB        | 0.76ms/0.1KB      |
| insert          | 10.85ms/32.1KB    | 45.99ms/318.4KB     | 21.00ms/318.0KB   |
| pop             | 0.87ms/0.1KB      | 1.39ms/0.1KB        | 1.49ms/0.1KB      |
| popitem         | 0.75ms/0.1KB      | 1.71ms/0.2KB        | 1.09ms/0.1KB      |
| setdefault      | 10.64ms/32.1KB    | 47.72ms/318.4KB     | 66.61ms/319.2KB   |
| update          | 6.55ms/1135.1KB   | 40.31ms/893.1KB     | 19.52ms/892.8KB   |

- 🥇 `cachebox.LRUCache`
- 🥈 `cacheing.LRUCache`
- 🥉 `cachetools.LRUCache`

### MRUCache 

| Operation\Class | cachebox.MRUCache | cachetools.MRUCache |
| --------------- | ----------------- | ------------------- |
| clear           | 13.31ms/0.1KB     | 43.63ms/0.9KB       |
| delete          | 1.71ms/0.1KB      | 1.04ms/0.1KB        |
| get             | 1.36ms/0.1KB      | 0.88ms/0.1KB        |
| insert          | 11.49ms/23.9KB    | 51.03ms/318.4KB     |
| pop             | 0.95ms/0.1KB      | 1.43ms/0.1KB        |
| popitem         | 0.77ms/0.1KB      | 1.73ms/0.2KB        |
| setdefault      | 10.88ms/23.9KB    | 50.76ms/318.4KB     |
| update          | 5.90ms/1135.1KB   | 47.11ms/893.1KB     |

- 🥇 `cachebox.MRUCache`
- 🥈 `cachetools.MRUCache`

### RRCache 

| Operation\Class | cachebox.RRCache | cachetools.RRCache | cacheing.RandomCache |
| --------------- | ---------------- | ------------------ | -------------------- |
| clear           | 9.44ms/0.1KB     | 73.50ms/8.3KB      | 42.08ms/5.2KB        |
| delete          | 0.79ms/0.1KB     | 0.91ms/0.1KB       | 1.50ms/5.1KB         |
| get             | 0.74ms/0.1KB     | 0.63ms/0.1KB       | 0.61ms/0.1KB         |
| insert          | 15.20ms/32.0KB   | 89.44ms/179.6KB    | 43.61ms/285.9KB      |
| pop             | 0.70ms/0.1KB     | 1.08ms/0.1KB       | 1.62ms/5.1KB         |
| popitem         | 1.04ms/0.1KB     | 5.56ms/8.3KB       | 2.64ms/5.2KB         |
| setdefault      | 14.31ms/32.1KB   | 91.87ms/179.6KB    | 62.98ms/286.6KB      |
| update          | 11.10ms/1135.1KB | 85.15ms/754.8KB    | 36.56ms/860.6KB      |

- 🥇 `cachebox.RRCache`
- 🥈 `cacheing.RandomCache`
- 🥉 `cachetools.RRCache`

### TTLCache 

| Operation\Class | cachebox.TTLCache | cachetools.TTLCache | cacheing.TTLCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.55ms/0.1KB      | 68.53ms/1.0KB       | 40.90ms/1.1KB     |
| delete          | 0.82ms/0.1KB      | 1.47ms/0.2KB        | 2.01ms/0.2KB      |
| get             | 0.78ms/0.1KB      | 1.08ms/0.2KB        | 2.08ms/0.2KB      |
| insert          | 11.22ms/32.1KB    | 103.38ms/406.7KB    | 62.21ms/1875.9KB  |
| pop             | 0.73ms/0.1KB      | 3.73ms/0.3KB        | 3.17ms/0.2KB      |
| popitem         | 0.76ms/0.1KB      | 4.90ms/0.4KB        | 1.24ms/0.1KB      |
| setdefault      | 10.03ms/32.1KB    | 135.07ms/404.5KB    | 134.05ms/1877.8KB |
| update          | 7.10ms/1135.1KB   | 103.68ms/981.4KB    | 54.04ms/2173.2KB  |

- 🥇 `cachebox.TTLCache`
- 🥈 `cacheing.TTLCache`
- 🥉 `cachetools.TTLCache`

### TTLCacheNoDefault 

| Operation\Class | cachebox.TTLCacheNoDefault | cacheing.VTTLCache |
| --------------- | -------------------------- | ------------------ |
| clear           | 8.43ms/0.1KB               | 39.27ms/1.2KB      |
| delete          | 0.90ms/0.1KB               | 2.95ms/0.2KB       |
| get             | 0.78ms/0.1KB               | 1.84ms/0.2KB       |
| insert          | 452.23ms/32.1KB            | 13005.77ms/1884.8KB|
| pop             | 0.77ms/0.1KB               | 4.17ms/0.2KB       |
| popitem         | 0.78ms/0.1KB               | 2.10ms/0.1KB       |
| setdefault      | 462.28ms/32.1KB            | 12936.32ms/1886.8KB|
| update          | 6.23ms/1135.1KB            | 13242.75ms/2742.1KB|

- 🥇 `cachebox.TTLCacheNoDefault`
- 🥈 `cacheing.VTTLCache`

> [!TIP]\
> According to this benchmark, In `cachebox.TTLCacheNoDefault` if you want to insert several values in a time, use `update` instead of `insert` or `__setitem__`.

## Run yourself
1. Download source from here.
```sh
git clone https://github.com/awolverp/cachebox-benchmark
cd cachebox-benchmark
```

2. Install/Upgrade requirements:
```sh
pip3 install -r -U requirements.txt
```

3. You can run benchmark using `make` script or manually:
```sh
# Make:
make

# Manually:
python3 main.py Cache FIFOCache LFUCache LRUCache MRUCache RRCache TTLCache TTLCacheNoDefault
```
