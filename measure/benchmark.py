import matplotlib.pyplot as plt
import matplotx
import typing
import array
import time
import gc


class PerfCtx:
    __slots__ = ("perf",)

    def __init__(self) -> None:
        self.perf = 0

    def __enter__(self) -> None:
        self.perf = time.perf_counter_ns()
        return

    def __exit__(self, *_) -> None:
        self.perf = time.perf_counter_ns() - self.perf
        return


class FuncProtocol(typing.Protocol):
    name: str

    def setup(self, range_n: int) -> None: ...
    def __call__(self, ctx: PerfCtx, n: int) -> None: ...
    def finalize(self) -> None: ...


def _plotter(
    title: str, xlabel: str, ylabel: str, path: str, *points: typing.Tuple[typing.Sequence, str]
):
    with plt.style.context(matplotx.styles.dracula):
        fig, ax = plt.subplots()

        for p in points:
            ax.plot(p[0][0], p[0][1], label=p[1])

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()

        fig.tight_layout()
        fig.savefig(path)


class Benchmark:
    __slots__ = ("name", "func", "range_n", "warm_up", "repeat", "_data")

    def __init__(
        self,
        name: str,
        func: FuncProtocol,
        range_n: int = 1000,
        warm_up: float = 2.0,
        repeat: int = 1000,
    ) -> None:
        self.name = name
        self.func = func
        self.range_n = range_n
        self.warm_up = warm_up
        self.repeat = repeat
        self._data = [array.array("L"), array.array("L")]

    def _repeat_call(self, n: int):
        times = []
        for _ in range(self.repeat):
            ctx = PerfCtx()
            self.func(ctx, n)
            assert ctx.perf, "you don't use PerfCtx in your function %r." % self.func.__name__
            times.append(ctx.perf)

        return min(times)

    def do(self, between: int = 0) -> None:
        # warming up ...
        print("Warming Up ...")
        gc.collect()
        time.sleep(self.warm_up)

        if hasattr(self.func, "setup"):
            self.func.setup(self.range_n)

        for n in range(1, self.range_n + 1, 1):
            t0 = self._repeat_call(n)

            self._data[0].append(n)
            self._data[1].append(t0)

        if hasattr(self.func, "finalize"):
            self.func.finalize()

        print(
            "Min: %d / Max: %d / Avg: %d"
            % (min(self._data[1]), max(self._data[1]), sum(self._data[1]) / len(self._data[1]))
        )

        between = between or int(len(self._data[0]) / 100)
        self._data[0] = self._data[0][::between]
        self._data[1] = self._data[1][::between]

    def plot(self, path: str) -> None:
        _plotter(self.name, "items", "time (ns)", path, (self._data, self.name))
