
### Cache 

| Operation\Class | cachebox.Cache | cachetools.Cache |
| --------------- | -------------- | ---------------- |
| clear           | 0.68ms/0.1KB   | 4.24ms/81.9KB    |
| delete          | 0.85ms/24.5KB  | 0.90ms/82.2KB    |
| get             | 0.77ms/24.7KB  | 0.59ms/82.4KB    |
| insert          | 0.76ms/24.7KB  | 1.42ms/82.4KB    |
| pop             | 0.70ms/25.1KB  | 1.09ms/82.8KB    |
| popitem         | 0.00ms/0.0KB   | 1.57ms/83.1KB    |
| setdefault      | 0.68ms/25.9KB  | 1.52ms/83.1KB    |
| update          | 0.27ms/70.8KB  | 1.06ms/130.9KB   |

### FIFOCache 

| Operation\Class | cachebox.FIFOCache | cachetools.FIFOCache |
| --------------- | ------------------ | -------------------- |
| clear           | 7.77ms/832.5KB     | 39.41ms/1207.9KB     |
| delete          | 0.81ms/832.5KB     | 1.02ms/1207.9KB      |
| get             | 0.76ms/832.5KB     | 0.60ms/1207.9KB      |
| insert          | 10.03ms/832.5KB    | 45.21ms/1207.9KB     |
| pop             | 0.68ms/832.5KB     | 1.20ms/1207.9KB      |
| popitem         | 0.77ms/832.5KB     | 1.59ms/1207.9KB      |
| setdefault      | 9.39ms/832.5KB     | 43.69ms/1207.9KB     |
| update          | 6.34ms/1207.9KB    | 39.53ms/1207.9KB     |

### LFUCache 

| Operation\Class | cachebox.LFUCache | cachetools.LFUCache | cacheing.LFUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 7.90ms/1207.9KB   | 171.24ms/1211.4KB   | 29.52ms/1211.4KB  |
| delete          | 0.83ms/1207.9KB   | 1.60ms/1211.4KB     | 1.06ms/1211.4KB   |
| get             | 0.79ms/1207.9KB   | 0.96ms/1211.4KB     | 1.09ms/1211.4KB   |
| insert          | 46.83ms/1207.9KB  | 1354.85ms/1211.4KB  | 25.34ms/1211.4KB  |
| pop             | 0.71ms/1207.9KB   | 2.17ms/1211.4KB     | 2.38ms/1211.4KB   |
| popitem         | 3.63ms/1207.9KB   | 30.03ms/1211.4KB    | 1.22ms/1211.4KB   |
| setdefault      | 43.00ms/1207.9KB  | 524.22ms/1211.4KB   | 46.30ms/1211.4KB  |
| update          | 39.85ms/1211.4KB  | 520.70ms/1211.4KB   | 17.59ms/1818.4KB  |

### LRUCache 

| Operation\Class | cachebox.LRUCache | cachetools.LRUCache | cacheing.LRUCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 8.79ms/1818.4KB   | 41.85ms/1818.4KB    | 33.95ms/1818.4KB  |
| delete          | 0.84ms/1818.4KB   | 1.07ms/1818.4KB     | 0.99ms/1818.4KB   |
| get             | 0.78ms/1818.4KB   | 0.83ms/1818.4KB     | 0.73ms/1818.4KB   |
| insert          | 10.16ms/1818.4KB  | 48.88ms/1818.4KB    | 20.85ms/1818.4KB  |
| pop             | 0.69ms/1818.4KB   | 1.49ms/1818.4KB     | 1.38ms/1818.4KB   |
| popitem         | 0.76ms/1818.4KB   | 1.77ms/1818.4KB     | 1.10ms/1818.4KB   |
| setdefault      | 8.94ms/1818.4KB   | 49.29ms/1818.4KB    | 53.73ms/1818.4KB  |
| update          | 5.85ms/1818.4KB   | 44.28ms/1818.4KB    | 15.62ms/1818.4KB  |

### MRUCache 

| Operation\Class | cachebox.MRUCache | cachetools.MRUCache |
| --------------- | ----------------- | ------------------- |
| clear           | 8.10ms/1818.4KB   | 39.85ms/1818.4KB    |
| delete          | 1.16ms/1818.4KB   | 1.05ms/1818.4KB     |
| get             | 0.77ms/1818.4KB   | 0.79ms/1818.4KB     |
| insert          | 9.90ms/1818.4KB   | 47.42ms/1818.4KB    |
| pop             | 0.95ms/1818.4KB   | 1.42ms/1818.4KB     |
| popitem         | 0.76ms/1818.4KB   | 1.79ms/1818.4KB     |
| setdefault      | 9.09ms/1818.4KB   | 46.78ms/1818.4KB    |
| update          | 5.92ms/1818.4KB   | 41.34ms/1818.4KB    |

### RRCache 

| Operation\Class | cachebox.RRCache | cachetools.RRCache |
| --------------- | ---------------- | ------------------ |
| clear           | 7.96ms/1818.4KB  | 78.13ms/1818.4KB   |
| delete          | 0.84ms/1818.4KB  | 0.90ms/1818.4KB    |
| get             | 0.91ms/1818.4KB  | 0.84ms/1818.4KB    |
| insert          | 14.70ms/1818.4KB | 97.48ms/1818.4KB   |
| pop             | 0.72ms/1818.4KB  | 1.07ms/1818.4KB    |
| popitem         | 1.06ms/1818.4KB  | 6.17ms/1818.4KB    |
| setdefault      | 13.46ms/1818.4KB | 97.24ms/1818.4KB   |
| update          | 12.30ms/1818.4KB | 91.32ms/1818.4KB   |

### TTLCache 

| Operation\Class | cachebox.TTLCache | cachetools.TTLCache | cacheing.TTLCache |
| --------------- | ----------------- | ------------------- | ----------------- |
| clear           | 9.01ms/1818.4KB   | 77.59ms/1818.4KB    | 38.14ms/2098.8KB  |
| delete          | 0.92ms/1818.4KB   | 1.67ms/1818.4KB     | 2.15ms/2123.8KB   |
| get             | 0.87ms/1818.4KB   | 1.03ms/1818.4KB     | 1.77ms/2275.7KB   |
| insert          | 12.37ms/1818.4KB  | 120.30ms/1818.4KB   | 67.42ms/3690.7KB  |
| pop             | 0.71ms/1818.4KB   | 4.93ms/1818.4KB     | 3.76ms/3716.1KB   |
| popitem         | 0.81ms/1818.4KB   | 6.53ms/1818.4KB     | 1.46ms/3868.0KB   |
| setdefault      | 10.32ms/1818.4KB  | 156.38ms/1818.4KB   | 150.07ms/5285.1KB |
| update          | 7.07ms/1818.4KB   | 115.73ms/1818.4KB   | 65.88ms/7170.2KB  |

### TTLCacheNoDefault 

| Operation\Class | cachebox.TTLCacheNoDefault | cacheing.VTTLCache |
| --------------- | -------------------------- | ------------------ |
| clear           | 7.98ms/7350.5KB            | 41.64ms/8107.6KB   |
| delete          | 0.91ms/7350.5KB            | 2.68ms/8107.6KB    |
| get             | 0.83ms/7350.5KB            | 2.64ms/8107.6KB    |
| insert          | 494.73ms/7350.5KB          | 12691.60ms/8107.6KB |
| pop             | 0.76ms/7350.5KB            | 3.95ms/8107.6KB    |
| popitem         | 0.80ms/7350.5KB            | 1.52ms/8107.6KB    |
| setdefault      | 480.64ms/7350.5KB          | 13129.20ms/8107.6KB |
| update          | 6.24ms/7726.8KB            | 12606.31ms/8107.6KB |

