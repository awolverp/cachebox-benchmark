import matplotlib.pyplot as plt
import typing
import time


plt.rcParams.update(
    {
        "ytick.color": "w",
        "xtick.color": "w",
        "axes.labelcolor": "w",
        "axes.edgecolor": "w",
        "figure.figsize": (11, 3),
    }
)


class Bencher:
    def __init__(self) -> None:
        self.performance = 0

        self._perf = None
        self._stopped = True

    def start(self):
        self._stopped = False
        self._perf = time.perf_counter()

    def stop(self):
        if self._stopped:
            return

        self._perf = time.perf_counter() - self._perf
        self._stopped = True
        self.performance += self._perf


class Benchmark:
    def __init__(self, title: str = None, xlabel: str = None, ylabel: str = None) -> None:
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.funcs = []  # type: list[tuple[str, typing.Callable[["Bencher"], None]]]
        self._stats = []  # type: list[tuple[str, float]]

    def add_bench(self, name: str, func: typing.Callable[["Bencher"], None]):
        self.funcs.append((name, func))

    def start(self, verbose: bool = True):
        if verbose and self.title:
                print(self.title, "(BENCHMARK)")

        for name, f in self.funcs:
            b = Bencher()
            f(b)

            assert b.performance is not None, "stop bencher at the end of your function"

            if verbose:
                print("* {} - Performance: {:.1f}ms".format(name, b.performance * 1000))

            self._stats.append((name, b.performance * 1000))

        return self._stats

    def plot_bar(self, filename: str):
        fig, ax = plt.subplots()
        bars = ax.barh([y for y, _ in self._stats], [x for _, x in self._stats], color="#6c5ce7")

        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#DDDDDD")
        ax.set_facecolor((0, 0, 0, 0))
        ax.tick_params(bottom=False, right=False)
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, color="#EEEEEE")
        ax.yaxis.grid(False)

        for bar in bars:
            ax.text(
                bar.get_width() + 0.01,
                bar.get_y() + bar.get_height() / 2,
                "{}ms".format(round(bar.get_width(), 1)),
                verticalalignment="center",
                color="#fff",
                weight="bold",
            )

        if self.title:
            ax.set_title(self.title, pad=15, color="#fff", weight="bold")

        if self.xlabel:
            ax.set_xlabel(self.xlabel, labelpad=15, color="#fff")

        if self.ylabel:
            ax.set_xlabel(self.ylabel, labelpad=15, color="#fff")

        fig.set_facecolor((0, 0, 0, 0))
        fig.tight_layout()
        fig.savefig(filename)
