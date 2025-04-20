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


class BadHash(int):
    def __hash__(self):
        return 1  # All objects has same hash


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
    if type_ is dict:
        return type_()

    if type_ in (
        cachebox.TTLCache,
        cachetools.TTLCache,
        cacheing.TTLCache,
    ):
        return type_(maxsize, 10)

    return type_(maxsize)


def get_dummy(cache_impl, delete = lambda cache, n: cache.__delitem__(n)):
    if isinstance(cache_impl, cachebox.VTTLCache):
        def dummy(n):
            cache_impl.insert(n, n, 100)
            delete(cache_impl, n)

    # elif isinstance(cache_impl, cacheing.VTTLCache):
    #     def dummy(n):
    #         cache_impl[(n, n+1)] = n
    #         delete(cache_impl, n)
    
    else:
        def dummy(n):
            cache_impl[n] = n
            delete(cache_impl, n)
    
    return dummy


@bench.benchmark()
def insertion(ctx: bench.Context, cache_impl):
    if isinstance(cache_impl, (dict, cachebox.Cache, cachetools.Cache)):
        range_n = 10000
    else:
        range_n = 100000

    if isinstance(cache_impl, cachebox.VTTLCache):
        setup = lambda _: random.randint(5, 10)

        def __setitem__(n, ttl):
            """
            Inserting elements into cache
            """
            cache_impl.insert(n, n, ttl)

    # elif isinstance(cache_impl, cacheing.VTTLCache):
    #     setup = lambda _: random.randint(5, 10)

    #     def __setitem__(n, ttl):
    #         """
    #         Inserting elements into cache
    #         """
    #         cache_impl[(n, ttl)] = n

    else:
        setup = None

        def __setitem__(n):
            """
            Inserting elements into cache
            """
            cache_impl[n] = n

    ctx.run(__setitem__, range_n, warmup=get_dummy(cache_impl), setup=setup)


@bench.benchmark()
def lookup(ctx: bench.Context, cache_impl):
    range_n = 10000

    # fill the cache
    for i in range(range_n):
        cache_impl[i] = i

    def get(n):
        """
        Lookup keys which are exist
        """
        cache_impl.get(n, "default")

    ctx.run(get, range_n, warmup=get_dummy(cache_impl, delete=lambda _, __: None))


@bench.benchmark()
def lookup_no_exists(ctx: bench.Context, cache_impl):
    range_n = 10000

    # fill the cache
    for i in range(range_n, range_n * 2):
        cache_impl[i] = i

    def get(n):
        """
        Lookup keys which does not exist
        """
        cache_impl.get(n, "default")

    ctx.run(get, range_n)


@bench.benchmark()
def deletion(ctx: bench.Context, cache_impl):
    range_n = 10000

    # fill the cache
    for i in range(range_n):
        cache_impl[i] = i

    def delete(n):
        """
        Deleting elements
        """
        del cache_impl[n]

    ctx.run(delete, range_n, warmup=get_dummy(cache_impl, delete=lambda _, __: None))


@bench.benchmark()
def popitem(ctx: bench.Context, cache_impl):
    if isinstance(cache_impl, (dict, cachebox.Cache, cachetools.Cache)):
        raise bench.SkipError
    
    range_n = 10000

    # fill the cache
    for i in range(range_n):
        cache_impl[i] = i

    def algorithm(n):
        """
        Popitem
        """
        cache_impl.popitem()

    ctx.run(algorithm, range_n, warmup=get_dummy(cache_impl, delete=lambda _, __: None))


@bench.benchmark()
def collision(ctx: bench.Context, cache_impl):
    range_n = 10000

    # fill the cache
    for i in range(range_n):
        cache_impl[BadHash(i)] = None

    def get_collision(n):
        """
        Lookup collision keys
        """
        cache_impl.get(BadHash(n))

    ctx.run(get_collision, range_n, warmup=get_dummy(cache_impl, delete=lambda _, __: None))


def _plot(name: str, res: list):
    with plt.style.context(matplotx.styles.dracula):
        plt.figure(figsize=(10, 6))

        for index, dt in enumerate(res):
            plt.bar(index, dt[3], label=dt[0])

        matplotx.show_bar_values("{:.0f}")

        plt.legend(
            title="Libs",
            bbox_to_anchor=(1.05, 1),  # Positions legend outside the plot
            loc="upper left",
            borderaxespad=0.0,
            frameon=False,
            fontsize=10,
        )

        plt.tight_layout()

        plt.title(name + " [in nanoseconds]")
        plt.savefig("photos/" + name + ".png")


if len(sys.argv) < 2:
    specific = ""
else:
    specific = sys.argv[1]


results = {}

for name, r in bench.run_benchmarks(specific):
    results[name] = r

print("\n:: Generating markdown file ...")
try:
    os.rename("README.md", "README.md.bak")
except FileNotFoundError:
    pass

file = mdutils.MdUtils("README.md")
file.new_header(1, "Caching libraries Benchmarks")
file.new_paragraph(
    "According to my new library [cachebox](https://github.com/awolverp/cachebox), I decided to benchmark caching libraries\n"
    "which are I know, to show the power of [cachebox](https://github.com/awolverp/cachebox) ...\n"
    "\n"
    "If you know other library, tell me to add it to this page.\n"
    "\n"
    "> [!NOTE]\\\n"
    f"> The system on which the benchmarks are done: {platform.platform()}\n\n"
    "> [!NOTE]\\\n"
    f"> The `cacheing.VTTLCache` class was excluded from the benchmark because of numerous unreasonable errors."
)

file.new_header(2, "Benchmarks")
file.new_paragraph(
    "**Versions**:\n"
    f"- Python: {platform.python_version()}\n"
    f"- cachebox version: {cachebox.__version__}\n"
    f"- cachetools version: {cachetools.__version__}\n"
    f"- cacheing version: N/A\n"
    f"- lru-dict: N/A\n"
)

for name, res in results.items():
    file.new_header(3, name)

    if len(res) > 1:
        _plot(name, res)
        file.new_paragraph(f"![{name}-image](photos/{name}.png)\n")

    items = ["Name", "min (ns)", "mean (ns)", "max (ns)", "stddev (ns)"]

    for a in res:
        items.extend((a[0], int(a[2]), int(a[3]), int(a[4]), int(a[5])))

    file.new_table(5, len(res) + 1, items)


file.new_header(2, "Run for yourself")
file.new_paragraph(
    """Clone repository with **git** (or download it from here):
```bash
git clone https://github.com/awolverp/cachebox-benchmark
```

Install requirements:
```bash
pip3 install -U -r requiremenets.txt
```

Run benchmark:
```bash
python3 main.py
```"""
)

file.create_md_file()
