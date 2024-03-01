from .benchmark import (
    Benchmark,
    CacheBenchmark,
    MultiBenchmark
)
from importlib import import_module

_original_methods = {
    "clear": (lambda obj, size: obj.update((i, i) for i in range(size)), lambda obj, n: obj.clear()),
    "delete": (lambda obj, size: obj.update((i, i) for i in range(size)), lambda obj, n: obj.__delitem__(n)),
    "get": (lambda obj, size: obj.update((i, i) for i in range(size)), lambda obj, n: obj.__getitem__(n)),
    "insert": lambda obj, n: obj.__setitem__(n, n),
    "pop": (lambda obj, size: obj.update((i, i) for i in range(size)), lambda obj, n: obj.pop(n, None)),
    "popitem": (lambda obj, size: obj.update((i, i) for i in range(size)), lambda obj, n: obj.popitem()),
    "setdefault": lambda obj, n: obj.setdefault(n, n),
    "update": lambda obj, n: obj.update({i:i for i in range(n)}),
}
_vttl_methods = {
    "clear": (lambda obj, size: obj.update(((i, 2), i) for i in range(size)), lambda obj, n: obj.clear()),
    "delete": (lambda obj, size: obj.update(((i, 2), i) for i in range(size)), lambda obj, n: obj.__delitem__(n)),
    "get": (lambda obj, size: obj.update(((i, 2), i) for i in range(size)), lambda obj, n: obj.__getitem__(n)),
    "insert": lambda obj, n: obj.__setitem__((n, n or 1), n),
    "pop": (lambda obj, size: obj.update(((i, 2), i) for i in range(size)), lambda obj, n: obj.pop(n, None)),
    "popitem": (lambda obj, size: obj.update(((i, 2), i) for i in range(size)), lambda obj, n: obj.popitem()),
    "setdefault": lambda obj, n: obj.setdefault((n, 2), n),
    "update": lambda obj, n: obj.update({(i, 2):i for i in range(n)}),
}
_ttlnodefault_methods = {
    "clear": (lambda obj, size: obj.update(((i, i) for i in range(size)), 2), lambda obj, n: obj.clear()),
    "delete": (lambda obj, size: obj.update(((i, i) for i in range(size)), 2), lambda obj, n: obj.__delitem__(n)),
    "get": (lambda obj, size: obj.update(((i, i) for i in range(size)), 2), lambda obj, n: obj.__getitem__(n)),
    "insert": lambda obj, n: obj.insert(n, n, n or 1),
    "pop": (lambda obj, size: obj.update(((i, i) for i in range(size)), 2), lambda obj, n: obj.pop(n, None)),
    "popitem": (lambda obj, size: obj.update(((i, i) for i in range(size)), 2), lambda obj, n: obj.popitem()),
    "setdefault": lambda obj, n: obj.setdefault(n, n, n or 1),
    "update": lambda obj, n: obj.update({i:i for i in range(n)}, 2),
}

def get_benchmark(name: str):
    # cachebox.Cache class is different, so has different benchmark attributes

    benchmarks = []

    for module in ["cachebox", "cachetools", "cacheing"]:
        module_t = import_module(module)
        
        if name == "TTLCacheNoDefault" and module == "cacheing":
            name = "VTTLCache"

        try:
            class_t = getattr(module_t, name)
        except AttributeError:
            print("> NOTE: {!r} module doesn't have {!r} class or anything like it, so ignored".format(module, name))
            continue

        kwargs = {"capacity": 1000} if module == "cacheing" else {"maxsize": 1000}
        if name == "TTLCache":
            kwargs["ttl"] = 2

        if name == "Cache":
            benchmarks.append(
                CacheBenchmark(
                    class_t,
                    _original_methods,
                    kwargs=kwargs
                )
            )
        
        elif name == "VTTLCache":
            benchmarks.append(
                Benchmark(
                    class_t,
                    _vttl_methods,
                    kwargs=kwargs
                )
            )
        
        elif name == "TTLCacheNoDefault":
            benchmarks.append(
                Benchmark(
                    class_t,
                    _ttlnodefault_methods,
                    kwargs=kwargs
                )
            )
        
        else:
            benchmarks.append(
                Benchmark(
                    class_t,
                    _original_methods,
                    kwargs=kwargs
                )
            )

    return MultiBenchmark(*benchmarks)
