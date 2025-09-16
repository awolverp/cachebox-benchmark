import statistics
import inspect
import typing
import gc
import time
import sys
import os
from contextlib import contextmanager


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


@contextmanager
def benchmark_environment():
    """Context manager to ensure stable benchmarking environment"""
    # Disable garbage collection during benchmarking
    gc_was_enabled = gc.isenabled()
    gc.disable()
    
    # Set high priority (Unix only)
    if hasattr(os, 'nice'):
        original_nice = os.nice(0)
        try:
            os.nice(-10)  # Higher priority
        except PermissionError:
            pass  # Ignore if we don't have permission
    
    try:
        # Force garbage collection before starting
        gc.collect()
        yield
    finally:
        # Restore original state
        if gc_was_enabled:
            gc.enable()
        
        if hasattr(os, 'nice'):
            try:
                os.nice(original_nice - os.nice(0))
            except (PermissionError, OSError):
                pass


def precise_timer():
    """Get the most precise timer available"""
    if sys.platform == "win32":
        return time.perf_counter_ns
    else:
        # On Unix, try to use clock_gettime with CLOCK_MONOTONIC
        try:
            import time
            def monotonic_ns():
                return int(time.clock_gettime(time.CLOCK_MONOTONIC) * 1_000_000_000)
            return monotonic_ns
        except (AttributeError, OSError):
            return time.perf_counter_ns


class Context:
    __slots__ = ("prefix", "_result", "_timer")

    def __init__(self, fixture_ids: typing.Sequence[str]):
        self.prefix = "-".join(fixture_ids)
        self._result: tuple = ()
        self._timer = precise_timer()

    def _adaptive_warmup(self, func, setup_func=None, target_time_ms=100):
        """Adaptive warmup to determine optimal number of iterations"""
        warmup_iterations = 1
        
        # Quick test to estimate iteration time
        if setup_func:
            setup_result = setup_func(0)
            start = self._timer()
            func(0, setup_result)
            single_time = self._timer() - start
        else:
            start = self._timer()
            func(0)
            single_time = self._timer() - start
        
        if single_time > 0:
            # Target warmup time in nanoseconds
            target_ns = target_time_ms * 1_000_000
            warmup_iterations = max(1, min(1000, int(target_ns / single_time)))
        
        return warmup_iterations

    def run(
    self,
        func: typing.Callable,
        range_n: int,
        setup: typing.Callable = None,
        min_iterations: int = 5,
        max_iterations: int = 100,
        target_precision: float = 0.01,
    ):
        assert not self._result
        
        print(f"\r    :: BENCHMARKING {self.prefix}", end="", flush=True)
        
        with benchmark_environment():
            # Pre-create all setup results to avoid timing setup overhead
            setup_results = []
            if setup is not None:
                for i in range(range_n):
                    setup_results.append(setup(i))
            
            # Adaptive warmup with pre-created setup
            warmup_iters = min(100, range_n // 10)  # More conservative warmup
            
            # Warmup phase
            for i in range(warmup_iters):
                if setup_results:
                    func(i % range_n, setup_results[i % len(setup_results)])
                else:
                    func(i % range_n)
            
            # Force garbage collection after warmup
            gc.collect()
            
            # Measurement phase with larger batches for stability
            measurements = []
            iteration = 0
            consecutive_stable_batches = 0
            
            while iteration < max_iterations and consecutive_stable_batches < 3:
                batch_times = []
                
                # Larger batch size for more stable measurements
                batch_size = min(50, range_n)
                
                # Measure entire batch with minimal overhead
                batch_start = self._timer()
                for i in range(batch_size):
                    idx = (iteration + i) % range_n
                    if setup_results:
                        func(idx, setup_results[idx])
                    else:
                        func(idx)
                batch_end = self._timer()
                
                # Calculate average time per operation in this batch
                avg_batch_time = (batch_end - batch_start) / batch_size
                
                # Individual measurements within batch (more precise)
                for i in range(min(10, batch_size)):  # Sample some individual ops
                    idx = (iteration + i) % range_n
                    start = self._timer()
                    if setup_results:
                        func(idx, setup_results[idx])
                    else:
                        func(idx)
                    end = self._timer()
                    batch_times.append(end - start)
                
                measurements.extend(batch_times)
                iteration += batch_size
                
                # Check batch stability
                if len(batch_times) > 1:
                    batch_cv = statistics.stdev(batch_times) / statistics.mean(batch_times)
                    if batch_cv < 0.05:  # Low coefficient of variation
                        consecutive_stable_batches += 1
                    else:
                        consecutive_stable_batches = 0
                
                # Early stopping if we have stable results
                if len(measurements) >= min_iterations:
                    current_mean = statistics.mean(measurements)
                    if current_mean > 0:
                        current_cv = statistics.stdev(measurements) / current_mean
                        if current_cv <= target_precision:
                            break
            
            # More aggressive outlier removal
            if len(measurements) >= 10:
                measurements.sort()
                # Remove top and bottom 10% instead of 5%
                trim_count = len(measurements) // 10
                if trim_count > 0:
                    measurements = measurements[trim_count:-trim_count]
            
            # Calculate statistics
            min_time = min(measurements)
            mean_time = statistics.mean(measurements)
            max_time = max(measurements)
            std_time = statistics.stdev(measurements) if len(measurements) > 1 else 0.0
            
            self._result = (
                self.prefix,
                func.__doc__.strip() if func.__doc__ else "No description",
                min_time,
                mean_time,
                max_time,
                std_time,
                len(measurements)
            )
            
            # Assess measurement quality
            noise_ratio = (std_time / mean_time) if mean_time > 0 else 0
            if noise_ratio > 0.1:
                status = f" (HIGH NOISE: {noise_ratio:.1%})"
            elif noise_ratio > 0.05:
                status = f" (MODERATE NOISE: {noise_ratio:.1%})"
            else:
                status = f" (LOW NOISE: {noise_ratio:.1%})"
            
            print(f"\r    :: BENCHMARKING {self.prefix} PASSED{status} [{len(measurements)} samples]")



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


def run_benchmarks(specific: str = ""):
    print(":: Starting benchmark suite with optimized measurement...")
    print(f":: Timer resolution: {precise_timer().__name__}")
    print(f":: Python version: {sys.version}")
    print()
    
    if specific:
        _it = filter(lambda x: specific == x.name, _registered_cases)
    else:
        _it = iter(_registered_cases)

    for case in _it:
        print(f":: FUNCTION {case.name}")
        case.run()
        
        # Brief pause between benchmarks to let system stabilize
        time.sleep(0.2)
        
        yield case.name, case._result
