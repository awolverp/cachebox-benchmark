import statistics
import inspect
import typing
import array
import timeit
import time


_registered_cases = []  # type: list[BenchmarkCase]
_registered_fixtures = {}  # type: dict[str, FixtureFunc]


class SkipError(Exception):
    pass


class FixtureResult:
    __slots__ = ("result", "id")

    def __init__(self, result, id: str):
        self.result = result
        self.id = id

    def __repr__(self):
        return f"FixtureResult(id={self.id}, result={self.result})"


class FixtureFunc:
    __slots__ = ("func", "objects", "ids")

    def __init__(self, func: typing.Callable, objects: typing.Sequence, ids: typing.Sequence[str]):
        self.func = func
        self.objects = objects
        self.ids = ids

    def __iter__(self):
        for obj, id in zip(self.objects, self.ids):
            yield FixtureResult(self.func(obj), id)


def fixture(
    objects: typing.Sequence, ids: typing.Sequence[str] = (), name: typing.Optional[str] = None
):
    if not ids:
        ids = []

        for i in objects:
            if isinstance(i, type):
                ids.append(f"{i.__module__.replace('._cachebox', '', 1)}.{i.__name__}")
            else:
                ids.append(repr(i))

    assert len(objects) == len(ids)

    def __inner(func: typing.Callable):
        _registered_fixtures[name or func.__name__] = FixtureFunc(func, objects, ids)
        return func

    return __inner


class Context:
    __slots__ = ("prefix", "_result")

    def __init__(self, fixture_ids: typing.Sequence[str]):
        self.prefix = "-".join(fixture_ids)
        self._result: tuple = ()

    def run(
        self,
        func: typing.Callable,
        range_n: int,
        setup: typing.Callable = None,
        warmup: typing.Callable = None,
        repeat: int = 1,
    ):
        assert not self._result
        data = array.array("L")

        print("\r    :: BENCHMARKING " + self.prefix, end="")

        if warmup is not None:
            for n in range(10):
                warmup(n)
                time.sleep(0.1)

        for i in range(range_n):
            if setup is not None:
                argument = setup(i)
            else:
                argument = None

            perf = timeit.timeit(
                stmt="func(i)" if argument is None else "func(i, argument)",
                number=repeat,
                globals={"func": func, "setup": setup, "i": i, "argument": argument},
                timer=time.perf_counter_ns,
            )

            data.append(perf)

        self._result = (
            self.prefix,
            func.__doc__.strip(),
            min(data),
            statistics.mean(data),
            max(data),
            # shows that there's noise or not.
            statistics.stdev(data),
        )

        if (self._result[5] / self._result[3]) > 0.2:
            print("\r    :: BENCHMARKING " + self.prefix + " PASSED (noises found)")
        else:
            print("\r    :: BENCHMARKING " + self.prefix + " PASSED")


class BenchmarkCase:
    __slots__ = ("func", "name", "_fixtures", "_result")

    def __init__(self, func: typing.Callable, name: str):
        self.func = func
        self.name = name
        self._fixtures = [
            _registered_fixtures[name]
            for name in inspect.signature(func).parameters.keys()
            if name != "ctx"
        ]

        self._result = []

    def _call_with_fixtures(self, params: typing.List[FixtureResult]):
        ctx = Context(tuple(i.id for i in params))
        params = tuple(i.result for i in params)

        try:
            self.func(ctx, *params)
        except SkipError:
            return

        assert ctx._result
        self._result.append(ctx._result)

    def _iter_fixture(self, params: typing.List[FixtureResult] = []):
        if not self._fixtures:
            return self._call_with_fixtures(params)

        index = len(params)
        if index >= len(self._fixtures):
            return self._call_with_fixtures(params)

        for obj in self._fixtures[index]:
            self._iter_fixture(params + [obj])

    def run(self):
        self._iter_fixture()


def benchmark(name: typing.Optional[str] = None):
    def __inner(func):
        case = BenchmarkCase(func, name or func.__name__)
        _registered_cases.append(case)
        return func

    return __inner


def run_benchmarks(
    specific: str = "",
):
    if specific:
        _it = filter(lambda x: specific == x.name, _registered_cases)
    else:
        _it = iter(_registered_cases)

    for case in _it:
        print(":: FUNCTION " + case.name)
        case.run()

        time.sleep(0.5)

        yield case.name, case._result
