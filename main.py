"""
Optimized Cache Library Benchmark Suite
Comprehensive performance testing with noise reduction and statistical rigor.
"""

import matplotlib.pyplot as plt
import matplotx
import cachetools
import cacheing
import cachebox
import lru
import mdutils
import sys
import os
import platform
from typing import Dict, List, Any
from dataclasses import dataclass

# Import optimized benchmark framework
from bench import benchmark, fixture, SkipError, BenchmarkResult, run_benchmarks


# Test configuration constants
SMALL_CACHE_SIZE = 1000  # For dict/unlimited caches
STANDARD_CACHE_SIZE = 10000  # For limited caches
LARGE_CACHE_SIZE = 50000  # For stress tests

# Test data sizes
INSERTION_OPS = 10000
LOOKUP_OPS = 5000
DELETION_OPS = 2000
COLLISION_OPS = 1000

# Fixed TTL values (no randomness)
SHORT_TTL = 10
LONG_TTL = 100


class BadHash(int):
    """Deterministic bad hash for collision testing"""

    def __hash__(self):
        return 42  # Fixed hash value for consistent collision behavior


@dataclass
class TestData:
    """Pre-computed test data to eliminate setup overhead"""

    keys: List[int]
    values: List[int]
    bad_hash_keys: List[BadHash]
    missing_keys: List[int]

    @classmethod
    def create(cls, size: int) -> "TestData":
        """Create deterministic test data"""
        # Use deterministic sequence instead of random
        keys = list(range(size))
        values = [i * 2 for i in range(size)]  # Simple deterministic values
        bad_hash_keys = [BadHash(i) for i in range(min(size, COLLISION_OPS))]
        missing_keys = list(range(size * 10, size * 11))  # Keys that won't exist

        return cls(keys, values, bad_hash_keys, missing_keys)


# Global test data instances (created once)
TEST_DATA_SMALL = TestData.create(SMALL_CACHE_SIZE)
TEST_DATA_STANDARD = TestData.create(STANDARD_CACHE_SIZE)
TEST_DATA_COLLISION = TestData.create(COLLISION_OPS)


class CacheManager:
    """Manages cache instances with proper initialization and cleanup"""

    def __init__(self, cache_type, maxsize: int):
        self.cache_type = cache_type
        self.maxsize = maxsize
        self.instances = []

    def create_cache(self) -> Any:
        """Create a new cache instance with proper parameters"""
        if self.cache_type is dict:
            cache = dict()
        elif self.cache_type in (cachebox.TTLCache, cachetools.TTLCache, cacheing.TTLCache):
            cache = self.cache_type(self.maxsize, SHORT_TTL)
        else:
            cache = self.cache_type(self.maxsize)

        self.instances.append(cache)
        return cache

    def get_populated_cache(self, data: TestData, use_long_ttl: bool = True) -> Any:
        """Get a pre-populated cache for lookup tests"""
        cache = self.create_cache()
        ttl_value = LONG_TTL if use_long_ttl else SHORT_TTL

        # Pre-populate with test data
        populate_count = min(
            len(data.keys), self.maxsize if self.maxsize < float("inf") else len(data.keys)
        )
        for i in range(populate_count):
            key, value = data.keys[i], data.values[i]

            if isinstance(cache, cachebox.VTTLCache):
                cache.insert(key, value, ttl_value)
            else:
                cache[key] = value

        return cache

    def cleanup(self):
        """Cleanup all created instances"""
        for cache in self.instances:
            try:
                cache.clear()
            except:
                pass
        self.instances.clear()


@fixture(
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
def cache_impl(cache_type):
    """Create cache implementation manager"""
    # Use smaller size for unlimited caches to prevent memory issues
    if cache_type in (dict, cachebox.Cache, cachetools.Cache):
        maxsize = SMALL_CACHE_SIZE
        test_data = TEST_DATA_SMALL
    else:
        maxsize = STANDARD_CACHE_SIZE
        test_data = TEST_DATA_STANDARD

    manager = CacheManager(cache_type, maxsize)
    manager.test_data = test_data
    return manager


@benchmark()
def insertion(ctx, cache_impl: CacheManager):
    """Optimized cache insertion benchmark"""
    test_data = cache_impl.test_data
    ops_count = min(len(test_data.keys), INSERTION_OPS)

    # Pre-create cache pool to minimize allocation overhead
    cache_pool = []
    pool_size = max(10, ops_count // 1000)  # Adaptive pool size

    def setup(iteration):
        # Reuse caches from pool, create new ones less frequently
        pool_idx = iteration // 100  # New cache every 100 operations

        while len(cache_pool) <= pool_idx:
            cache_pool.append(cache_impl.create_cache())

        cache = cache_pool[pool_idx]
        key_idx = iteration % len(test_data.keys)
        key, value = test_data.keys[key_idx], test_data.values[key_idx]

        # Add some offset to avoid key conflicts within same cache
        unique_key = key + (iteration // 100) * 100000

        if isinstance(cache, cachebox.VTTLCache):
            return cache, unique_key, value, SHORT_TTL
        else:
            return cache, unique_key, value, None

    def insert_op(n, setup_data):
        """Optimized insertion operation"""
        cache, key, value, ttl = setup_data

        if ttl is not None:
            cache.insert(key, value, ttl)
        else:
            cache[key] = value

    ctx.run(insert_op, ops_count, setup=setup)


@benchmark()
def lookup_existing(ctx, cache_impl: CacheManager):
    """Optimized existing key lookup benchmark"""
    test_data = cache_impl.test_data

    # Pre-populate cache once
    cache = cache_impl.get_populated_cache(test_data)
    available_keys = test_data.keys[
        : min(len(test_data.keys), len(cache) if hasattr(cache, "__len__") else len(test_data.keys))
    ]

    def setup(iteration):
        # Simple key cycling, no expensive operations
        key = available_keys[iteration % len(available_keys)]
        return cache, key

    def lookup_op(n, setup_data):
        """Optimized lookup operation"""
        cache, key = setup_data
        result = cache.get(key, None)  # Using .get() for consistency

    ctx.run(lookup_op, LOOKUP_OPS, setup=setup)


@benchmark()
def lookup_missing(ctx, cache_impl: CacheManager):
    """Optimized missing key lookup benchmark"""
    test_data = cache_impl.test_data

    # Pre-populate cache with existing keys
    cache = cache_impl.get_populated_cache(test_data)
    missing_keys = test_data.missing_keys

    def setup(iteration):
        # Cycle through missing keys
        key = missing_keys[iteration % len(missing_keys)]
        return cache, key

    def lookup_op(n, setup_data):
        """Optimized missing lookup operation"""
        cache, key = setup_data
        result = cache.get(key, "default")

    ctx.run(lookup_op, LOOKUP_OPS, setup=setup)


@benchmark()
def deletion(ctx, cache_impl: CacheManager):
    """Optimized deletion benchmark"""
    if isinstance(cache_impl.cache_type, type) and issubclass(cache_impl.cache_type, dict):
        if cache_impl.cache_type is dict:
            pass  # dict supports deletion
        else:
            # Some cache types might not support deletion
            try:
                test_cache = cache_impl.create_cache()
                test_cache[1] = 1
                del test_cache[1]
            except (NotImplementedError, AttributeError):
                raise SkipError("Cache type does not support deletion")

    test_data = cache_impl.test_data

    # Create multiple pre-populated caches for deletion
    cache_pool = []
    keys_per_cache = 100

    def setup(iteration):
        pool_idx = iteration // keys_per_cache

        # Create new cache when needed
        while len(cache_pool) <= pool_idx:
            cache = cache_impl.create_cache()

            # Pre-populate this cache
            start_idx = len(cache_pool) * keys_per_cache
            for i in range(keys_per_cache):
                if start_idx + i >= len(test_data.keys):
                    break
                key, value = test_data.keys[start_idx + i], test_data.values[start_idx + i]

                if isinstance(cache, cachebox.VTTLCache):
                    cache.insert(key, value, LONG_TTL)
                else:
                    cache[key] = value

            cache_pool.append(cache)

        cache = cache_pool[pool_idx]
        key_idx = (iteration % keys_per_cache) + (pool_idx * keys_per_cache)
        if key_idx < len(test_data.keys):
            key = test_data.keys[key_idx]
        else:
            key = test_data.keys[iteration % len(test_data.keys)]

        return cache, key

    def delete_op(n, setup_data):
        """Optimized deletion operation"""
        cache, key = setup_data
        try:
            del cache[key]
        except KeyError:
            pass  # Key might already be deleted

    ctx.run(delete_op, DELETION_OPS, setup=setup)


@benchmark()
def popitem(ctx, cache_impl: CacheManager):
    """Optimized popitem benchmark"""
    # Skip for unlimited caches
    if cache_impl.cache_type in (dict, cachebox.Cache, cachetools.Cache):
        raise SkipError("Unlimited caches don't need popitem testing")

    test_data = cache_impl.test_data

    def setup(iteration):
        # Create cache and overfill it to ensure popitem has work
        cache = cache_impl.create_cache()

        # Fill beyond capacity
        fill_count = int(cache_impl.maxsize * 1.5)
        for i in range(fill_count):
            key_idx = i % len(test_data.keys)
            key, value = (
                test_data.keys[key_idx] + i * 10000,
                test_data.values[key_idx],
            )  # Unique keys

            if isinstance(cache, cachebox.VTTLCache):
                cache.insert(key, value, LONG_TTL)
            else:
                cache[key] = value

        return cache

    def popitem_op(n, setup_data):
        """Optimized popitem operation"""
        cache = setup_data
        try:
            cache.popitem()
        except KeyError:
            # Cache is empty, add a few items and try again
            for i in range(5):
                unique_key = n * 1000 + i
                if isinstance(cache, cachebox.VTTLCache):
                    cache.insert(unique_key, i, LONG_TTL)
                else:
                    cache[unique_key] = i
            cache.popitem()

    ctx.run(popitem_op, 1000, setup=setup)


@benchmark()
def hash_collision(ctx, cache_impl: CacheManager):
    """Optimized hash collision benchmark"""
    test_data = TEST_DATA_COLLISION

    # Pre-populate cache with bad hash keys
    cache = cache_impl.create_cache()
    for i, bad_key in enumerate(test_data.bad_hash_keys):
        if isinstance(cache, cachebox.VTTLCache):
            cache.insert(bad_key, i, LONG_TTL)
        else:
            cache[bad_key] = i

    def setup(iteration):
        # Cycle through bad hash keys for consistent collision testing
        key = test_data.bad_hash_keys[iteration % len(test_data.bad_hash_keys)]
        return cache, key

    def collision_lookup_op(n, setup_data):
        """Collision lookup operation"""
        cache, key = setup_data
        result = cache.get(key)

    ctx.run(collision_lookup_op, COLLISION_OPS, setup=setup)


def generate_performance_plot(name: str, results: List[BenchmarkResult]):
    """Single beautiful plot per benchmark (replaces the 2x2 grid).
    - Bars: mean time (ns) with std errorbars (log scale)
    - Color by stability (green/orange/red)
    - Secondary axis: throughput (ops/sec, shown as Mops/sec line + markers)
    - Small ranking text box for top-3
    Saves to photos/{name}.png
    """
    if not results:
        return

    # Sort by mean time (fastest first)
    results = sorted(results, key=lambda r: r.mean_ns)
    labels = [r.name.split("-")[-1] for r in results]
    means = [r.mean_ns for r in results]
    stds = [r.std_ns for r in results]
    ops_per_sec = [r.ops_per_sec for r in results]

    try:
        style_ctx = matplotx.styles.aura["dark"]
    except Exception:
        style_ctx = None

    if style_ctx is not None:
        plt_style = plt.style.context(style_ctx)
    else:
        plt_style = plt.style.context("seaborn-darkgrid")

    with plt_style:
        fig, ax = plt.subplots(figsize=(14, 7))

        x = range(len(labels))
        
        bar_containers = ax.bar(
            x,
            means,
            yerr=stds,
            capsize=6,
            linewidth=0.8,
            edgecolor="#222222",
            color="#1762A4",
            alpha=0.95,
        )

        # Log scale for time to span wide ranges nicely
        ax.set_yscale("log")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=11)
        ax.set_ylabel("Execution time (ns) — log scale", fontsize=12)
        ax.set_title(f"{name.replace('_', ' ').title()}", fontsize=16, fontweight="bold", pad=12)

        # light grid lines
        ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)

        # Annotate each bar with human-friendly time
        for rect, mean in zip(bar_containers, means):
            height = rect.get_height()
            ypos = height * (1.18 if height > 0 else 1.0)
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                ypos,
                f"{int(mean):,} ns",
                ha="center",
                va="bottom",
                fontsize=9,
                rotation=0,
                color="black",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85),
            )

        # Secondary axis for throughput (ops/sec) -> show in Mops/sec line + markers
        ax2 = ax.twinx()
        ops_m = [o / 1e6 for o in ops_per_sec]
        ax2.plot(x, ops_m, marker="o", linestyle="-", linewidth=2, markersize=6, label="Throughput (Mops/s)", zorder=20, color="#3498DB")
        ax2.set_ylabel("Throughput (Mops/sec)", fontsize=12)
        ax2.set_ylim(bottom=0)
        # small throughput labels
        for xi, opm in zip(x, ops_m):
            ax2.text(xi, opm, f"{opm:.2f}M", ha="center", va="bottom", fontsize=9)

        # remove legend and textbox as requested (clean, minimal)
        plt.tight_layout()

        # Save figure with transparent background
        os.makedirs("photos", exist_ok=True)
        outpath = f"photos/{name}.png"
        plt.savefig(outpath, dpi=250, bbox_inches="tight")
        plt.close(fig)



def generate_comprehensive_report(all_results: Dict[str, List[BenchmarkResult]]):
    """Generate comprehensive markdown report"""
    try:
        if os.path.exists("README.md"):
            os.rename("README.md", "README.md.backup")
    except FileNotFoundError:
        pass

    # Calculate overall performance scores
    overall_scores = {}
    for benchmark_name, results in all_results.items():
        for result in results:
            impl_name = result.name.split("-")[-1]
            if impl_name not in overall_scores:
                overall_scores[impl_name] = []

            # Score based on relative performance (lower time = higher score)
            if results:
                min_time = min(r.mean_ns for r in results)
                relative_perf = min_time / result.mean_ns
                stability_bonus = 1.0 if result.is_stable else 0.8
                score = relative_perf * stability_bonus
                overall_scores[impl_name].append(score)

    file = mdutils.MdUtils("README.md")

    file.new_header(1, "Caching libraries Benchmarks")

    file.new_paragraph(
        "According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries\n"
        "which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...\n"
        "\n"
        "If you know other library, tell me to add it to this page.\n"
        "\n"
        "> [!NOTE]\\\n"
        "> The `cacheing.VTTLCache` class was excluded from the benchmark because of numerous unreasonable errors."
    )

    # System info
    file.new_paragraph(
        f"\n## 🖥️ System Information\n"
        f"- **Platform**: {platform.platform()}\n"
        f"- **Python**: {platform.python_version()}\n"
        f"- **Processor**: {platform.processor()}\n"
        f"- **Libraries**:\n"
        f"  - cachebox: {getattr(cachebox, '__version__', 'Unknown')}\n"
        f"  - cachetools: {getattr(cachetools, '__version__', 'Unknown')}\n"
        f"  - cacheing: 0.1.1\n"
        f"  - lru-dict: 1.3.0\n"
    )

    # Detailed results for each benchmark
    for benchmark_name, results in all_results.items():
        if not results:
            continue

        file.new_header(2, f"📊 {benchmark_name.replace('_', ' ').title()}")
        file.new_paragraph(f"![{benchmark_name}](photos/{benchmark_name}.png)")

        # Performance summary
        fastest = min(results, key=lambda r: r.mean_ns)
        slowest = max(results, key=lambda r: r.mean_ns)
        performance_range = slowest.mean_ns / fastest.mean_ns

        file.new_paragraph(
            f"- **Performance Range**: {performance_range:.1f}x difference between fastest and slowest\n"
            f"- **Best**: {fastest.name.split('-')[-1]} ({fastest.mean_ns:.0f}ns, {fastest.ops_per_sec / 1e6:.1f}M ops/sec)\n"
            f"- **Analysis**: {len([r for r in results if r.is_stable])} of {len(results)} implementations show stable measurements\n\n"
        )

        # Detailed table
        headers = [
            "Implementation",
            "Mean (ns)",
            "Std Dev (ns)",
            "Ops/sec",
            "Samples",
            "Stability",
            "Grade",
        ]
        table_rows = [] # type: list[list[str]]

        # Sort by performance
        sorted_results = sorted(results, key=lambda r: r.mean_ns)

        for result in sorted_results:
            impl_name = result.name.split("-")[-1]
            stability_emoji = (
                "🟢" if result.noise_ratio < 0.02 else "🟡" if result.noise_ratio < 0.05 else "🔴"
            )

            table_rows.append(
                [
                    impl_name,
                    f"{result.mean_ns:,.0f}",
                    f"{result.std_ns:,.0f}",
                    f"{result.ops_per_sec / 1e6:.1f}M",
                    str(result.samples),
                    f"{result.noise_ratio * 100:.1f}%",
                    f"{stability_emoji} {result.stability_grade}",
                ]
            )
        
        file.new_table(
            len(headers),
            len(table_rows) + 1,
            headers + [x for xs in table_rows for x in xs],
        )

    # Usage instructions
    file.new_header(2, "🚀 Usage")
    file.new_paragraph(
        "### Prerequisites\n"
        "```bash\n"
        "uv sync\n"
        "```\n\n"
        "### Run Benchmarks\n"
        "```bash\n"
        "# All benchmarks\n"
        "python main.py\n\n"
        "# Specific benchmark\n"
        "python main.py insertion\n"
        "python main.py lookup_existing\n"
        "```\n\n"
        "### Understanding Results\n\n"
        "- **🟢 Excellent (A+)**: <2% noise ratio - Highly reliable measurements\n"
        "- **🟡 Good (A-B)**: 2-10% noise ratio - Acceptable reliability\n"
        "- **🔴 Poor (C-D)**: >10% noise ratio - Less reliable measurements\n\n"
        "**Performance Metrics**:\n"
        "- **Mean (ns)**: Average execution time in nanoseconds\n"
        "- **Ops/sec**: Operations per second (throughput)\n"
        "- **Stability**: Measurement consistency (lower noise = more stable)\n"
    )

    file.create_md_file()
    print("📝 Generated comprehensive README.md")


def main():
    """Enhanced main benchmark execution"""
    specific_benchmark = sys.argv[1] if len(sys.argv) > 1 else ""

    print("🚀 STARTING OPTIMIZED CACHE BENCHMARK SUITE")
    print("=" * 80)

    all_results = {}

    try:
        for benchmark_name, results in run_benchmarks(specific_benchmark):
            all_results[benchmark_name] = results

            # Generate plot for this benchmark
            if results:
                generate_performance_plot(benchmark_name, results)
                print(f"📊 Generated plot: photos/{benchmark_name}.png")

        print("\n" + "=" * 80)
        print("📈 GENERATING COMPREHENSIVE ANALYSIS")
        print("=" * 80)

        # Generate comprehensive report
        generate_comprehensive_report(all_results)

        # Performance summary
        total_benchmarks = len(all_results)
        total_results = sum(len(results) for results in all_results.values())
        stable_results = sum(
            len([r for r in results if r.is_stable]) for results in all_results.values()
        )

        print(f"\n✅ BENCHMARK SUITE COMPLETED!")
        print(f"📊 {total_benchmarks} benchmarks, {total_results} implementations tested")
        print(
            f"🎯 {stable_results}/{total_results} ({stable_results / total_results * 100:.1f}%) stable measurements"
        )
        print(f"📁 Results saved to photos/ and README.md")

    except KeyboardInterrupt:
        print("\n❌ Benchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error during benchmarking: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
