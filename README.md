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
- cachebox version: 2.0.0
- cachetools version: 5.3.3
- cacheing version: 0.1.1


### Cache 

| Operation\Class | cachebox.Cache | cachetools.Cache | Python dictionary |
| --------------- | -------------- | ---------------- | ----------------- |
| clear           | 2.39ms/0.1KB   | 15.22ms/0.8KB    | 1.94ms/0.1KB      |
| delete          | 2.91ms/0.1KB   | 3.17ms/0.1KB     | 2.69ms/0.1KB      |
| get             | 1.16ms/0.1KB   | 2.23ms/0.1KB     | 1.08ms/0.1KB      |
| insert          | 2.82ms/23.8KB  | 5.08ms/69.0KB    | 1.17ms/69.0KB     |
| pop             | 2.19ms/0.1KB   | 1.11ms/0.1KB     | 0.64ms/0.1KB      |
| popitem         | N/A            | 6.23ms/0.2KB     | 1.26ms/0.1KB      |
| setdefault      | 3.04ms/23.8KB  | 4.27ms/69.0KB    | 1.16ms/69.0KB     |
| update          | 0.28ms/69.2KB  | 2.64ms/116.6KB   | 0.65ms/97.6KB     |

- 🥇 `dict` (Python dictionary)
- 🥈 `cachebox.Cache`
- 🥉 `cachetools.Cache`

### FIFOCache 

| Operation\Class | cachebox.FIFOCache | cachetools.FIFOCache |
| --------------- | ------------------ | -------------------- |
| clear           | 19.26ms/0.1KB      | 40.29ms/0.9KB        |
| delete          | 3.05ms/0.1KB       | 3.61ms/0.1KB         |
| get             | 0.75ms/0.1KB       | 2.55ms/0.1KB         |
| insert          | 27.26ms/32.1KB     | 58.43ms/318.4KB      |
| pop             | 2.36ms/0.1KB       | 4.36ms/0.1KB         |
| popitem         | 2.25ms/0.1KB       | 1.87ms/0.2KB         |
| setdefault      | 21.46ms/32.1KB     | 53.58ms/318.4KB      |
| update          | 11.40ms/609.2KB    | 53.06ms/893.1KB      |

- 🥇 `cachebox.FIFOCache`
- 🥈 `cachetools.FIFOCache`

### LFUCache 

| Operation\Class | cachebox.LFUCache | cachetools.LFUCache | cacheing.LFUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.24ms/0.1KB      | 122.71ms/1.0KB      | 31.81ms/0.9KB     |
| delete          | 2.69ms/0.1KB      | 5.97ms/0.2KB        | 3.70ms/0.1KB      |
| get             | 0.75ms/0.1KB      | 3.26ms/0.1KB        | 3.71ms/109.3KB    |
| insert          | 41.34ms/28.1KB    | 499.09ms/253.3KB    | 26.46ms/392.0KB   |
| pop             | 2.53ms/0.1KB      | 7.60ms/0.2KB        | 6.36ms/0.7KB      |
| popitem         | 6.29ms/0.1KB      | 42.61ms/0.4KB       | 4.78ms/0.1KB      |
| setdefault      | 36.12ms/28.1KB    | 529.11ms/253.3KB    | 51.57ms/393.0KB   |
| update          | 32.19ms/609.2KB   | 522.91ms/828.0KB    | 32.23ms/966.7KB   |

- 🥇 `cachebox.LFUCache`
- 🥈 `cacheing.LFUCache`
- 🥉 `cachetools.LFUCache`

### LRUCache 

| Operation\Class | cachebox.LRUCache | cachetools.LRUCache | cacheing.LRUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 19.56ms/0.1KB     | 40.87ms/0.9KB       | 35.04ms/0.9KB     |
| delete          | 2.69ms/0.1KB      | 3.56ms/0.1KB        | 3.48ms/0.1KB      |
| get             | 2.56ms/0.1KB      | 2.84ms/0.1KB        | 2.48ms/0.1KB      |
| insert          | 24.51ms/32.1KB    | 47.54ms/318.4KB     | 24.26ms/318.0KB   |
| pop             | 2.59ms/0.1KB      | 4.76ms/0.1KB        | 4.27ms/0.1KB      |
| popitem         | 2.72ms/0.1KB      | 6.42ms/0.2KB        | 3.87ms/0.1KB      |
| setdefault      | 11.65ms/32.1KB    | 48.90ms/318.4KB     | 57.07ms/319.2KB   |
| update          | 10.96ms/609.2KB   | 53.94ms/893.1KB     | 30.90ms/892.8KB   |

- 🥇 `cachebox.LRUCache`
- 🥈 `cacheing.LRUCache`
- 🥉 `cachetools.LRUCache`

### RRCache 

| Operation\Class | cachebox.RRCache | cachetools.RRCache | cacheing.RandomCache |
| --------------- | ---------------- | ------------------ | -------------------- |
| clear           | 11.01ms/0.1KB    | 73.69ms/8.3KB      | 41.80ms/5.2KB        |
| delete          | 2.79ms/0.1KB     | 3.24ms/0.1KB       | 5.50ms/5.1KB         |
| get             | 2.48ms/0.1KB     | 2.32ms/0.1KB       | 2.22ms/0.1KB         |
| insert          | 17.73ms/32.1KB   | 92.84ms/179.6KB    | 56.59ms/285.9KB      |
| pop             | 2.71ms/0.1KB     | 1.36ms/0.1KB       | 5.70ms/5.1KB         |
| popitem         | 3.48ms/0.1KB     | 17.88ms/8.3KB      | 5.66ms/5.2KB         |
| setdefault      | 27.53ms/32.1KB   | 95.28ms/179.6KB    | 76.93ms/286.6KB      |
| update          | 21.05ms/609.2KB  | 100.09ms/754.3KB   | 50.43ms/860.6KB      |

- 🥇 `cachebox.RRCache`
- 🥈 `cacheing.RandomCache`
- 🥉 `cachetools.RRCache`

### TTLCache 

| Operation\Class | cachebox.TTLCache | cachetools.TTLCache | cacheing.TTLCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 18.99ms/0.1KB     | 69.69ms/1.0KB       | 39.10ms/1.1KB     |
| delete          | 0.84ms/0.1KB      | 4.96ms/0.2KB        | 7.75ms/0.2KB      |
| get             | 3.02ms/0.1KB      | 1.92ms/0.2KB        | 5.51ms/0.2KB      |
| insert          | 24.60ms/32.1KB    | 149.43ms/406.7KB    | 73.92ms/1878.3KB  |
| pop             | 1.09ms/0.1KB      | 11.87ms/0.3KB       | 10.68ms/0.2KB     |
| popitem         | 0.88ms/0.1KB      | 5.36ms/0.4KB        | 1.88ms/0.1KB      |
| setdefault      | 19.37ms/32.1KB    | 149.49ms/404.5KB    | 152.02ms/1877.9KB |
| update          | 12.53ms/609.2KB   | 123.74ms/981.4KB    | 67.87ms/2173.3KB  |

- 🥇 `cachebox.TTLCache`
- 🥈 `cacheing.TTLCache`
- 🥉 `cachetools.TTLCache`

### VTTLCache 

| Operation\Class | cachebox.VTTLCache | cacheing.VTTLCache |
| --------------- | ------------------ | ------------------ |
| clear           | 19.08ms/0.1KB      | 37.61ms/1.1KB      |
| delete          | 3.40ms/0.1KB       | 2.03ms/0.2KB       |
| get             | 2.66ms/0.1KB       | 1.64ms/0.2KB       |
| insert          | 327.82ms/32.1KB    | 13140.41ms/1884.7KB |
| pop             | 3.26ms/0.1KB       | 3.22ms/0.2KB       |
| popitem         | 2.74ms/0.1KB       | 1.26ms/0.1KB       |
| setdefault      | 327.67ms/32.1KB    | 13992.55ms/1886.5KB |
| update          | 10.99ms/609.2KB    | 13820.60ms/2631.1KB |

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
