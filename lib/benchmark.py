import typing
import time
import tracemalloc

T = typing.TypeVar("T")


class Benchmark:
    def __init__(
        self,
        cache: typing.Type[T],
        methods: typing.Dict[str, typing.Tuple[typing.Callable[[T, int], typing.Any], typing.Callable[[T, int], typing.Any]]],
        kwargs={},
        name: str = "",
    ) -> None:
        self.name = name or "{}.{}".format(cache.__module__.replace("._cachebox", ""), cache.__name__)
        self.cache = cache
        self.kwargs = kwargs
        self.methods = methods

        self._results = {}

        self._n_range = 10000

    def _call_method(self, name: str):
        obj = self.cache(**self.kwargs)
        method = self.methods[name]

        n_range = self._n_range if not name.startswith(("pop", "delete", "popitem", "get")) else 1000

        if isinstance(method, tuple):
            setup, method = method
            setup(obj, n_range)

        if name.startswith("update"):
            tracemalloc.start()
            perf = time.perf_counter()

            try:
                method(obj, n_range)
            except NotImplementedError:
                self._results[name] = (0.0, 0.0)
                tracemalloc.stop()
                return
        
            perf = time.perf_counter() - perf
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        
        else:
            tracemalloc.start()
            perf = time.perf_counter()

            for n in range(n_range):
                try:
                    method(obj, n)
                except NotImplementedError:
                    self._results[name] = (0.0, 0.0)
                    tracemalloc.stop()
                    return
                
                except KeyError:
                    print(f"> NOTE: {self.name}.{name} method only tested for {n} items")
                    break
        
            perf = time.perf_counter() - perf
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        self._results[name] = (perf * 1000, peak/10**3)

    def compile(self):
        for methodname in self.methods.keys():
            time.sleep(0.5)
            self._call_method(methodname)


class CacheBenchmark(Benchmark):
    def __init__(
        self,
        cache: typing.Type[T],
        methods: typing.Dict[str, typing.Callable[[T, int], typing.Any]],
        kwargs={},
        name: str = "",
    ) -> None:
        super().__init__(cache, methods, kwargs, name)
        self._n_range = 1000


class MultiBenchmark:
    def __init__(self, *benchmarks: Benchmark) -> None:
        self.methods = sorted(benchmarks[0].methods.keys())

        for i in benchmarks:
            assert sorted(i.methods.keys()) == self.methods, f"i.methods != self.methods ({i.name})"
        
        self.benchmarks = benchmarks
        self._compiled = False
    
    def compile(self):
        if self._compiled:
            return
        
        for i in self.benchmarks:
            i.compile()

    def to_markdown(self):
        self.compile()
        
        headers = ["Operation\\Class"] + list(i.name for i in self.benchmarks)

        # generate headers
        text = "| " + " | ".join(headers) + " |\n"
        text += "| " + " | ".join(("-" * len(i)) for i in headers) + " |\n"

        # add methods
        for method in self.methods:
            text += "| {}{} | ".format(method, " " * abs(len(headers[0]) - len(method)))

            results = []
            for bench in self.benchmarks:
                results.append("{:.2f}ms/{:.1f}KB".format(bench._results[method][0], bench._results[method][1]))

            text += " | ".join(
                "{}{}".format(res, " " * (len(headers[index]) - len(res))) for index, res in enumerate(results, start=1)
            )

            text += " |\n"

        return text
