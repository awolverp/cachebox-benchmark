import matplotlib.pyplot as plt
import matplotx
import cachetools
import cacheing
import cachebox
import lru
import mdutils
import bench
import sys
import os
import platform
import random
import gc
import time


class BadHash(int):
    """Class for testing hash collision performance"""
    def __hash__(self):
        return 1  # All objects have same hash


@bench.fixture(
    objects=[
        dict,
        cachebox.Cache,
        cachetools.Cache,
        cachebox.FIFOCache,
        cachetools.FIFOCache,
        cachebox.LRUCache,
        cachetools.LRUCache,
        lru.LRU,
        cacheing.LRUCache,
        cachebox.LFUCache,
        cacheing.LFUCache,
        cachetools.LFUCache,
        cachebox.RRCache,
        cacheing.RandomCache,
        cachetools.RRCache,
        cachebox.TTLCache,
        cachetools.TTLCache,
        cacheing.TTLCache,
        cachebox.VTTLCache,
    ],
)
def cache_impl(type_, maxsize: int = 10000):
    """Create cache implementation with appropriate parameters"""
    if type_ is dict:
        return type_()

    if type_ in (cachebox.TTLCache, cachetools.TTLCache, cacheing.TTLCache):
        return type_(maxsize, 10)  # 10 second TTL

    return type_(maxsize)


def create_fresh_cache(cache_type, maxsize: int = 10000):
    """Create a fresh cache instance for each test"""
    return cache_impl(cache_type, maxsize)


@bench.benchmark()
def insertion(ctx: bench.Context, cache_impl):
    """Test insertion performance with clean cache for each measurement"""
    cache_type = type(cache_impl)
    
    # Determine appropriate test size
    if isinstance(cache_impl, (dict, cachebox.Cache, cachetools.Cache)):
        range_n = 1000  # Reduced for unbounded caches to avoid memory issues
    else:
        range_n = 10000
    
    def setup(iteration):
        # Create fresh cache for each measurement to avoid cache state interference
        fresh_cache = create_fresh_cache(cache_type)
        
        if isinstance(fresh_cache, cachebox.VTTLCache):
            ttl = random.randint(5, 15)
            return fresh_cache, ttl
        else:
            return fresh_cache, None
    
    def insert_op(n, setup_result):
        """Inserting elements into cache"""
        cache, ttl_or_none = setup_result
        
        if isinstance(cache, cachebox.VTTLCache):
            cache.insert(n, n, ttl_or_none)
        else:
            cache[n] = n
    
    ctx.run(insert_op, range_n, setup=setup, min_iterations=10, max_iterations=50)


@bench.benchmark()
def lookup_existing(ctx: bench.Context, cache_impl):
    """Test lookup performance for existing keys"""
    cache_type = type(cache_impl)
    range_n = 5000
    
    def setup(iteration):
        # Create cache and pre-populate it
        cache = create_fresh_cache(cache_type, maxsize=range_n * 2)
        
        # Pre-populate cache
        for i in range(range_n):
            if isinstance(cache, cachebox.VTTLCache):
                cache.insert(i, i, 100)  # Long TTL
            else:
                cache[i] = i
        
        # Return cache and the key to lookup
        return cache, iteration % range_n
    
    def lookup_op(n, setup_result):
        """Lookup keys which exist"""
        cache, key = setup_result
        cache.get(key, "default")
    
    ctx.run(lookup_op, range_n, setup=setup, min_iterations=15)


@bench.benchmark()
def lookup_missing(ctx: bench.Context, cache_impl):
    """Test lookup performance for non-existing keys"""
    cache_type = type(cache_impl)
    range_n = 5000
    
    def setup(iteration):
        # Create cache and pre-populate with different keys
        cache = create_fresh_cache(cache_type, maxsize=range_n)
        
        # Pre-populate with keys that won't be looked up
        offset = range_n * 2
        for i in range(range_n):
            if isinstance(cache, cachebox.VTTLCache):
                cache.insert(i + offset, i + offset, 100)
            else:
                cache[i + offset] = i + offset
        
        return cache, iteration % range_n  # These keys don't exist
    
    def lookup_missing_op(n, setup_result):
        """Lookup keys which do not exist"""
        cache, key = setup_result
        cache.get(key, "default")
    
    ctx.run(lookup_missing_op, range_n, setup=setup, min_iterations=15)


@bench.benchmark()
def deletion(ctx: bench.Context, cache_impl):
    """Test deletion performance"""
    cache_type = type(cache_impl)
    range_n = 5000
    
    def setup(iteration):
        # Create fresh cache and populate it
        cache = create_fresh_cache(cache_type, maxsize=range_n * 2)
        
        for i in range(range_n):
            if isinstance(cache, cachebox.VTTLCache):
                cache.insert(i, i, 100)
            else:
                cache[i] = i
        
        return cache, iteration % range_n
    
    def delete_op(n, setup_result):
        """Deleting elements"""
        cache, key = setup_result
        try:
            del cache[key]
        except KeyError:
            pass  # Key might already be deleted
    
    ctx.run(delete_op, range_n, setup=setup, min_iterations=10)


@bench.benchmark()
def popitem(ctx: bench.Context, cache_impl):
    """Test popitem performance"""
    if isinstance(cache_impl, (dict, cachebox.Cache, cachetools.Cache)):
        raise bench.SkipError  # Skip for unlimited caches
    
    cache_type = type(cache_impl)
    range_n = 2000
    
    def setup(iteration):
        # Create fresh cache and populate it well beyond capacity
        cache = create_fresh_cache(cache_type, maxsize=1000)
        
        # Populate beyond maxsize to ensure popitem has work to do
        for i in range(1500):
            if isinstance(cache, cachebox.VTTLCache):
                cache.insert(i, i, 100)
            else:
                cache[i] = i
        
        return cache
    
    def popitem_op(n, setup_result):
        """Popitem operation"""
        cache = setup_result
        try:
            cache.popitem()
        except KeyError:
            # Cache is empty, add some items
            for i in range(10):
                if isinstance(cache, cachebox.VTTLCache):
                    cache.insert(n * 10 + i, i, 100)
                else:
                    cache[n * 10 + i] = i
            cache.popitem()
    
    ctx.run(popitem_op, range_n, setup=setup, min_iterations=10)


@bench.benchmark()
def hash_collision(ctx: bench.Context, cache_impl):
    """Test performance under hash collisions"""
    cache_type = type(cache_impl)
    range_n = 1000  # Smaller for collision test
    
    def setup(iteration):
        # Create cache and populate with BadHash objects
        cache = create_fresh_cache(cache_type, maxsize=range_n * 2)
        
        for i in range(range_n):
            bad_hash_key = BadHash(i)
            if isinstance(cache, cachebox.VTTLCache):
                cache.insert(bad_hash_key, i, 100)
            else:
                cache[bad_hash_key] = i
        
        return cache, BadHash(iteration % range_n)
    
    def collision_lookup_op(n, setup_result):
        """Lookup with collision keys"""
        cache, key = setup_result
        cache.get(key)
    
    ctx.run(collision_lookup_op, range_n, setup=setup, min_iterations=10)


def _plot(name: str, res: list):
    """Generate performance comparison plots"""
    if not res:
        return
        
    with plt.style.context(matplotx.styles.dracula):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Mean performance plot
        labels = [dt[0] for dt in res]
        means = [dt[3] for dt in res]
        
        bars1 = ax1.bar(range(len(labels)), means)
        ax1.set_title(f'{name} - Mean Performance (ns)')
        ax1.set_xticks(range(len(labels)))
        ax1.set_xticklabels(labels, rotation=45, ha='right')
        ax1.set_ylabel('Time (nanoseconds)')
        
        # Add value labels on bars
        for bar, mean in zip(bars1, means):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(means)*0.01,
                    f'{int(mean)}', ha='center', va='bottom', fontsize=8)
        
        # Standard deviation plot (relative)
        rel_stdevs = [dt[5]/dt[3]*100 if dt[3] > 0 else 0 for dt in res]
        bars2 = ax2.bar(range(len(labels)), rel_stdevs)
        ax2.set_title(f'{name} - Measurement Stability (%)')
        ax2.set_xticks(range(len(labels)))
        ax2.set_xticklabels(labels, rotation=45, ha='right')
        ax2.set_ylabel('Relative Standard Deviation (%)')
        
        # Color code stability bars
        for bar, rel_stdev in zip(bars2, rel_stdevs):
            if rel_stdev > 10:
                bar.set_color('red')
            elif rel_stdev > 5:
                bar.set_color('orange')
            else:
                bar.set_color('green')
        
        plt.tight_layout()
        
        # Ensure photos directory exists
        os.makedirs("photos", exist_ok=True)
        plt.savefig(f"photos/{name}.png", dpi=150, bbox_inches='tight')
        plt.close()


def main():
    """Main benchmark execution function"""
    if len(sys.argv) < 2:
        specific = ""
    else:
        specific = sys.argv[1]

    print("=" * 60)
    print("CACHE LIBRARY BENCHMARK SUITE")
    print("=" * 60)
    print(f"Platform: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    print(f"Processor: {platform.processor()}")
    print("=" * 60)
    print()

    results = {}

    for name, r in bench.run_benchmarks(specific):
        results[name] = r
        print()

    print("=" * 60)
    print("GENERATING RESULTS...")
    print("=" * 60)

    # Generate plots
    for name, res in results.items():
        if len(res) > 1:
            _plot(name, res)
            print(f"Generated plot: photos/{name}.png")

    # Generate markdown report
    print("\n:: Generating comprehensive markdown report...")
    
    try:
        os.rename("README.md", "README.md.bak")
    except FileNotFoundError:
        pass

    file = mdutils.MdUtils("README.md")
    file.new_header(1, "Optimized Cache Library Benchmarks")
    file.new_paragraph(
        "Comprehensive benchmarks of Python caching libraries using an optimized measurement framework.\n"
        f"Based on [cachebox](https://github.com/awolverp/cachebox) performance comparisons.\n\n"
        
        "## Benchmark Methodology\n\n"
        "- **Adaptive warmup**: Automatically determines optimal warmup iterations\n"
        "- **Noise reduction**: Disables GC during measurements, uses high-resolution timers\n"
        "- **Statistical rigor**: Multiple samples with outlier removal and precision targeting\n"
        "- **Fresh state**: Each measurement uses a clean cache instance\n"
        "- **Realistic workloads**: Tests use appropriate data sizes and access patterns\n\n"
        
        f"**System Information:**\n"
        f"- Platform: {platform.platform()}\n"
        f"- Python: {platform.python_version()}\n"
        f"- Processor: {platform.processor()}\n\n"
        
        "**Library Versions:**\n"
        f"- cachebox: {cachebox.__version__}\n"
        f"- cachetools: {cachetools.__version__}\n"
        f"- cacheing: Available\n"
        f"- lru-dict: Available\n"
    )

    for name, res in results.items():
        file.new_header(2, name.replace('_', ' ').title())
        
        if len(res) > 1:
            file.new_paragraph(f"![{name}-performance](photos/{name}.png)\n")

        # Enhanced table with additional metrics
        headers = ["Implementation", "Min (ns)", "Mean (ns)", "Max (ns)", "StdDev (ns)", "Samples", "Stability"]
        table_data = [headers]

        for result in res:
            stability = "🟢 Excellent" if result[5]/result[3] < 0.05 else \
                       "🟡 Good" if result[5]/result[3] < 0.10 else \
                       "🔴 Poor"
            
            table_data.append([
                result[0],
                f"{int(result[2]):,}",
                f"{int(result[3]):,}",
                f"{int(result[4]):,}",
                f"{int(result[5]):,}",
                str(result[6]) if len(result) > 6 else "N/A",
                stability
            ])

        # Create table
        for row in table_data[1:]:
            file.new_table_row(row)
        
        file.new_line()

    file.new_header(2, "Running the Benchmarks")
    file.new_paragraph(
        """### Prerequisites
```bash
pip install -r requirements.txt
```

### Run All Benchmarks
```bash
python main.py
```

### Run Specific Benchmark
```bash
python main.py insertion
python main.py lookup_existing
python main.py hash_collision
```

### Understanding the Results

- **Min/Mean/Max**: Minimum, average, and maximum execution times
- **StdDev**: Standard deviation indicating measurement consistency
- **Samples**: Number of measurements taken for statistical confidence
- **Stability**: Color-coded measurement reliability indicator
  - 🟢 Excellent: <5% relative standard deviation
  - 🟡 Good: 5-10% relative standard deviation  
  - 🔴 Poor: >10% relative standard deviation"""
    )

    file.create_md_file()
    print("Generated comprehensive README.md")
    
    if os.path.exists("README.md.bak"):
        print("Previous README.md backed up as README.md.bak")

    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()