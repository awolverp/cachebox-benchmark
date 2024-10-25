from .benchmark import Benchmark, _plotter


class GroupBenchmark:
    __slots__ = ("benches", "name")

    def __init__(self, name: str, *benches: Benchmark) -> None:
        self.name = name
        self.benches = benches

    def do(self, between: int = 0) -> None:
        print("-" * 20)
        for b in self.benches:
            print("(group %r) Benchmarking %r ..." % (self.name, b.name))
            b.do(between=between)

    def plot(self, path: str) -> None:
        points = tuple((b._data, b.name) for b in self.benches)
        _plotter(self.name, "items", "time (ns)", path, *points)
