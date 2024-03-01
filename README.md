# Caching libraries Benchmarks
According to my new library [cachebox](https://github.com/awolverp/cachebox), i decided to benchmark caching libraries
i know, to show my library power ...

**Qualification criteria is:**
- Needs to support minimum 2 alghoritms
- Runs on Python3.8+

If you know other library, tell me to add to this page.

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
| clear           | 0.83ms/0.1KB   | 4.36ms/81.9KB    |
| delete          | 0.88ms/24.5KB  | 0.91ms/82.1KB    |
| insert          | 0.77ms/24.5KB  | 1.43ms/82.1KB    |
| pop             | 0.70ms/24.9KB  | 1.07ms/82.6KB    |
| popitem         | 0.00ms/0.0KB   | 1.57ms/82.8KB    |
| setdefault      | 0.70ms/25.5KB  | 1.52ms/82.8KB    |
| update          | 0.29ms/70.6KB  | 1.05ms/130.7KB   |

### FIFOCache 

| Operation\Class | cachebox.FIFOCache | cachetools.FIFOCache |
| --------------- | ------------------ | -------------------- |
| clear           | 8.04ms/832.1KB     | 39.95ms/1208.2KB     |
| delete          | 0.83ms/832.1KB     | 1.03ms/1208.2KB      |
| insert          | 10.24ms/832.1KB    | 43.89ms/1208.2KB     |
| pop             | 0.69ms/832.1KB     | 1.19ms/1208.2KB      |
| popitem         | 0.78ms/832.1KB     | 1.59ms/1208.2KB      |
| setdefault      | 8.91ms/832.1KB     | 43.98ms/1208.2KB     |
| update          | 6.09ms/1208.2KB    | 38.72ms/1208.2KB     |

### LFUCache 

| Operation\Class | cachebox.LFUCache | cachetools.LFUCache | cacheing.LFUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.02ms/1208.2KB   | 185.07ms/1212.9KB   | 29.77ms/1212.9KB  |
| delete          | 0.84ms/1208.2KB   | 2.49ms/1212.9KB     | 1.09ms/1212.9KB   |
| insert          | 43.55ms/1208.2KB  | 1349.47ms/1212.9KB  | 22.03ms/1212.9KB  |
| pop             | 0.69ms/1208.2KB   | 2.15ms/1212.9KB     | 1.75ms/1212.9KB   |
| popitem         | 3.55ms/1208.2KB   | 29.33ms/1212.9KB    | 1.30ms/1212.9KB   |
| setdefault      | 42.44ms/1208.2KB  | 504.67ms/1212.9KB   | 48.40ms/1212.9KB  |
| update          | 38.78ms/1212.9KB  | 494.83ms/1212.9KB   | 17.00ms/1658.6KB  |

### LRUCache 

| Operation\Class | cachebox.LRUCache | cachetools.LRUCache | cacheing.LRUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.02ms/1658.6KB   | 39.31ms/1658.6KB    | 32.06ms/1658.6KB  |
| delete          | 0.82ms/1658.6KB   | 1.03ms/1658.6KB     | 0.99ms/1658.6KB   |
| insert          | 9.98ms/1658.6KB   | 45.73ms/1658.6KB    | 19.72ms/1658.6KB  |
| pop             | 0.69ms/1658.6KB   | 1.39ms/1658.6KB     | 1.22ms/1658.6KB   |
| popitem         | 0.75ms/1658.6KB   | 1.78ms/1658.6KB     | 1.10ms/1658.6KB   |
| setdefault      | 8.95ms/1658.6KB   | 45.26ms/1658.6KB    | 52.73ms/1658.6KB  |
| update          | 5.79ms/1658.6KB   | 39.44ms/1658.6KB    | 15.79ms/1658.6KB  |

### MRUCache 

| Operation\Class | cachebox.MRUCache | cachetools.MRUCache |
| --------------- | ----------------- | ------------------- |
| clear           | 8.08ms/1658.6KB   | 39.53ms/1658.6KB    |
| delete          | 1.05ms/1658.6KB   | 1.04ms/1658.6KB     |
| insert          | 9.86ms/1658.6KB   | 46.51ms/1658.6KB    |
| pop             | 0.91ms/1658.6KB   | 1.42ms/1658.6KB     |
| popitem         | 0.77ms/1658.6KB   | 1.77ms/1658.6KB     |
| setdefault      | 8.76ms/1658.6KB   | 52.65ms/1658.6KB    |
| update          | 5.72ms/1658.6KB   | 40.44ms/1658.6KB    |

### RRCache 

| Operation\Class | cachebox.RRCache | cachetools.RRCache |
| --------------- | ---------------- | ------------------ |
| clear           | 8.13ms/1658.6KB  | 75.05ms/1658.6KB   |
| delete          | 0.84ms/1658.6KB  | 0.94ms/1658.6KB    |
| insert          | 14.79ms/1658.6KB | 93.17ms/1658.6KB   |
| pop             | 0.70ms/1658.6KB  | 1.06ms/1658.6KB    |
| popitem         | 1.09ms/1658.6KB  | 5.87ms/1658.6KB    |
| setdefault      | 13.71ms/1658.6KB | 92.13ms/1658.6KB   |
| update          | 11.80ms/1658.6KB | 87.23ms/1658.6KB   |

### TTLCache 

| Operation\Class | cachebox.TTLCache | cachetools.TTLCache | cacheing.TTLCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.25ms/1658.6KB   | 73.55ms/1658.6KB    | 41.72ms/1976.4KB  |
| delete          | 0.92ms/1658.6KB   | 1.63ms/1658.6KB     | 2.32ms/2001.3KB   |
| insert          | 15.80ms/1658.6KB  | 120.09ms/1658.6KB   | 74.64ms/3568.1KB  |
| pop             | 1.22ms/1658.6KB   | 5.23ms/1658.6KB     | 3.84ms/3593.4KB   |
| popitem         | 1.44ms/1658.6KB   | 5.99ms/1658.6KB     | 1.30ms/3745.3KB   |
| setdefault      | 13.96ms/1658.6KB  | 151.74ms/1658.6KB   | 151.67ms/5162.3KB |
| update          | 6.96ms/1658.6KB   | 119.57ms/1658.6KB   | 67.23ms/7047.6KB  |

### TTLCacheNoDefault 

| Operation\Class | cachebox.TTLCacheNoDefault | cacheing.VTTLCache |
| --------------- | -------------------------- | ------------------ |
| clear           | 8.57ms/7227.7KB            | 50.28ms/8357.2KB   |
| delete          | 1.32ms/7227.7KB            | 2.58ms/8357.2KB    |
| insert          | 454.86ms/7227.7KB          | 12737.40ms/8357.2KB |
| pop             | 1.29ms/7227.7KB            | 4.09ms/8357.2KB    |
| popitem         | 1.37ms/7227.7KB            | 1.59ms/8357.2KB    |
| setdefault      | 501.72ms/7227.7KB          | 13350.88ms/8357.2KB |
| update          | 6.74ms/7603.8KB            | 12751.64ms/8357.2KB |

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
