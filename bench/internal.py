"""
Optimized benchmarking framework with noise reduction techniques.
Based on industry best practices for micro-benchmarking.
"""

import statistics
import inspect
import typing
import gc
import time
import sys
import os
import math
from contextlib import contextmanager
from dataclasses import dataclass
from typing import List, Optional, Callable, Any


_registered_cases = []
_registered_fixtures = {}

# Global constants for benchmarking
MIN_MEASUREMENT_TIME_NS = 1_000_000  # 1ms minimum per measurement batch
TARGET_TOTAL_TIME_NS = 100_000_000  # 100ms total measurement time
MIN_SAMPLES = 30  # Minimum statistical samples
MAX_SAMPLES = 1000  # Maximum samples to prevent infinite loops
OUTLIER_THRESHOLD = 2.5  # Z-score threshold for outlier removal


class SkipError(Exception):
    """Exception to skip a benchmark"""

    pass


@dataclass
class BenchmarkResult:
    """Structured benchmark result"""

    name: str
    description: str
    min_ns: float
    mean_ns: float
    max_ns: float
    std_ns: float
    samples: int
    noise_ratio: float
    ops_per_sec: float

    @property
    def is_stable(self) -> bool:
        """Check if measurements are stable (low noise)"""
        return self.noise_ratio < 0.05

    @property
    def stability_grade(self) -> str:
        """Get stability grade"""
        if self.noise_ratio < 0.02:
            return "A+ (Excellent)"
        elif self.noise_ratio < 0.05:
            return "A (Very Good)"
        elif self.noise_ratio < 0.10:
            return "B (Good)"
        elif self.noise_ratio < 0.20:
            return "C (Fair)"
        else:
            return "D (Poor)"


class FixtureResult:
    __slots__ = ("result", "id")

    def __init__(self, result, id: str):
        self.result = result
        self.id = id

    def __repr__(self):
        return f"FixtureResult(id={self.id})"


class FixtureFunc:
    __slots__ = ("func", "objects", "ids")

    def __init__(self, func: Callable, objects: typing.Sequence, ids: typing.Sequence[str]):
        self.func = func
        self.objects = objects
        self.ids = ids

    def __iter__(self):
        for obj, id in zip(self.objects, self.ids):
            yield FixtureResult(self.func(obj), id)


def fixture(objects: typing.Sequence, ids: typing.Sequence[str] = (), name: Optional[str] = None):
    """Register a fixture for benchmarking"""
    if not ids:
        ids = []
        for i in objects:
            if isinstance(i, type):
                module_name = i.__module__.replace("._cachebox", "", 1)
                ids.append(f"{module_name}.{i.__name__}")
            else:
                ids.append(repr(i))

    assert len(objects) == len(ids), "objects and ids must have same length"

    def __inner(func: Callable):
        _registered_fixtures[name or func.__name__] = FixtureFunc(func, objects, ids)
        return func

    return __inner


class TimerCalibration:
    """Calibrate timer overhead and resolution"""

    def __init__(self):
        self.timer_func = time.perf_counter_ns
        self.overhead_ns = self._measure_overhead()
        self.resolution_ns = self._measure_resolution()

    def _measure_overhead(self) -> float:
        """Measure timer call overhead"""
        measurements = []
        timer = self.timer_func

        # Warm up timer
        for _ in range(100):
            timer()

        # Measure overhead
        for _ in range(1000):
            start = timer()
            end = timer()
            measurements.append(end - start)

        # Use minimum as best estimate of pure overhead
        return min(measurements)

    def _measure_resolution(self) -> float:
        """Measure timer resolution"""
        timer = self.timer_func
        last_time = timer()

        # Find smallest non-zero difference
        for _ in range(10000):
            current_time = timer()
            diff = current_time - last_time
            if diff > 0:
                return diff
            last_time = current_time

        return 1.0  # Fallback: assume 1ns resolution


# Global timer calibration
_TIMER = TimerCalibration()


@contextmanager
def benchmark_environment():
    """Create optimal benchmarking environment"""
    # Store original state
    gc_was_enabled = gc.isenabled()

    # Disable garbage collection and clean up
    gc.disable()
    gc.collect()

    # Set process priority (cross-platform)
    try:
        if sys.platform == "win32":
            import psutil

            process = psutil.Process()
            original_priority = process.nice()
            process.nice(psutil.HIGH_PRIORITY_CLASS)
        else:
            original_nice = os.nice(0) if hasattr(os, "nice") else 0
            if hasattr(os, "nice"):
                os.nice(-10)  # Increase priority
    except (ImportError, PermissionError, OSError):
        pass

    # Set CPU affinity to reduce context switching
    original_affinity = None
    try:
        if sys.platform != "darwin":  # macOS doesn't support this
            import psutil

            process = psutil.Process()
            original_affinity = process.cpu_affinity()
            # Pin to first CPU core
            process.cpu_affinity([original_affinity[0]])
    except (ImportError, AttributeError, OSError):
        pass

    # Warm up CPU to stable frequency (important for modern CPUs)
    warmup_start = time.perf_counter()
    warmup_target = warmup_start + 0.5  # 500ms warmup
    iteration = 0
    while time.perf_counter() < warmup_target:
        # Light computational load to warm up CPU
        math.sqrt(iteration)
        iteration += 1

    try:
        yield
    finally:
        # Restore original state
        if gc_was_enabled:
            gc.enable()

        # Restore process priority
        try:
            if sys.platform == "win32" and "original_priority" in locals():
                import psutil

                process = psutil.Process()
                process.nice(original_priority)
            elif hasattr(os, "nice") and "original_nice" in locals():
                current_nice = os.nice(0)
                os.nice(original_nice - current_nice)
        except (ImportError, PermissionError, OSError):
            pass

        # Restore CPU affinity
        if original_affinity is not None:
            try:
                import psutil

                process = psutil.Process()
                process.cpu_affinity(original_affinity)
            except (ImportError, OSError):
                pass


def remove_outliers_iqr(data: List[float]) -> List[float]:
    """Remove outliers using Interquartile Range method"""
    if len(data) < 4:
        return data

    sorted_data = sorted(data)
    n = len(sorted_data)
    q1_idx = n // 4
    q3_idx = 3 * n // 4

    q1 = sorted_data[q1_idx]
    q3 = sorted_data[q3_idx]
    iqr = q3 - q1

    if iqr == 0:
        return data

    # Standard IQR outlier detection
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return [x for x in data if lower_bound <= x <= upper_bound]


def remove_outliers_zscore(data: List[float], threshold: float = OUTLIER_THRESHOLD) -> List[float]:
    """Remove outliers using Z-score method"""
    if len(data) < 3:
        return data

    mean_val = statistics.mean(data)
    std_val = statistics.stdev(data) if len(data) > 1 else 0

    if std_val == 0:
        return data

    return [x for x in data if abs((x - mean_val) / std_val) <= threshold]


class Context:
    """Optimized benchmark execution context"""

    __slots__ = ("prefix", "_result", "_timer_func", "_timer_overhead")

    def __init__(self, fixture_ids: typing.Sequence[str]):
        self.prefix = "-".join(fixture_ids)
        self._result: Optional[BenchmarkResult] = None
        self._timer_func = _TIMER.timer_func
        self._timer_overhead = _TIMER.overhead_ns

    def _estimate_operation_time(self, func: Callable, setup_data: Any = None) -> float:
        """Estimate single operation time"""
        # Warmup
        for _ in range(10):
            if setup_data is not None:
                func(0, setup_data)
            else:
                func(0)

        # Quick measurement
        measurements = []
        for i in range(20):
            start = self._timer_func()
            if setup_data is not None:
                func(i, setup_data)
            else:
                func(i)
            end = self._timer_func()
            measurements.append(end - start - self._timer_overhead)

        return statistics.median([max(1, m) for m in measurements])

    def _run_batch_measurement(
        self, func: Callable, batch_size: int, setup_data_list: List[Any]
    ) -> List[float]:
        """Run batch measurements for very fast operations"""
        measurements = []

        # Calculate how many batches we need
        target_batches = max(MIN_SAMPLES, min(MAX_SAMPLES, 100))

        for batch_idx in range(target_batches):
            # Prepare batch indices
            start_idx = (batch_idx * batch_size) % len(setup_data_list) if setup_data_list else 0

            # Measure entire batch
            batch_start = self._timer_func()
            for i in range(batch_size):
                data_idx = (start_idx + i) % len(setup_data_list) if setup_data_list else i
                if setup_data_list:
                    func(data_idx, setup_data_list[data_idx])
                else:
                    func(data_idx)
            batch_end = self._timer_func()

            # Calculate per-operation time
            total_time = batch_end - batch_start - (self._timer_overhead * batch_size)
            per_op_time = max(1.0, total_time / batch_size)

            measurements.append(per_op_time)

        return measurements

    def _run_individual_measurement(
        self, func: Callable, target_samples: int, setup_data_list: List[Any]
    ) -> List[float]:
        """Run individual measurements for slower operations"""
        measurements = []

        for i in range(target_samples):
            data_idx = i % len(setup_data_list) if setup_data_list else i

            start = self._timer_func()
            if setup_data_list:
                func(data_idx, setup_data_list[data_idx])
            else:
                func(data_idx)
            end = self._timer_func()

            # Subtract overhead and ensure positive
            measured_time = max(1.0, end - start - self._timer_overhead)
            measurements.append(measured_time)

        return measurements

    def run(
        self,
        func: Callable,
        range_n: int,
        setup: Optional[Callable] = None,
        min_samples: int = MIN_SAMPLES,
        max_samples: int = MAX_SAMPLES,
    ):
        """Run optimized benchmark with adaptive measurement strategy"""

        if self._result is not None:
            raise RuntimeError("Context already used")

        print(f"\r    :: BENCHMARKING {self.prefix} ", end="", flush=True)

        with benchmark_environment():
            # Pre-create setup data to eliminate setup overhead during measurement
            setup_data_list = []
            if setup is not None:
                # Limit setup data to reasonable size to avoid memory pressure
                setup_count = min(range_n, 1000)
                for i in range(setup_count):
                    setup_data_list.append(setup(i))

            # Estimate operation time to choose measurement strategy
            sample_setup = setup_data_list[0] if setup_data_list else None
            estimated_time = self._estimate_operation_time(func, sample_setup)

            # Choose measurement strategy based on operation speed
            if estimated_time < 100:  # Very fast operations (< 100ns)
                batch_size = max(100, MIN_MEASUREMENT_TIME_NS // max(1, int(estimated_time)))
                measurements = self._run_batch_measurement(func, batch_size, setup_data_list)
                measurement_type = "batch"
            else:
                # For slower operations, use individual measurements
                target_samples = min(
                    max_samples,
                    max(min_samples, TARGET_TOTAL_TIME_NS // max(1, int(estimated_time))),
                )
                measurements = self._run_individual_measurement(
                    func, target_samples, setup_data_list
                )
                measurement_type = "individual"

            # Advanced outlier removal
            original_count = len(measurements)

            # First pass: IQR method
            measurements = remove_outliers_iqr(measurements)

            # Second pass: Z-score method if we still have enough data
            if len(measurements) >= min_samples:
                measurements = remove_outliers_zscore(measurements)

            # Ensure we have minimum samples
            if len(measurements) < min_samples:
                print(f"WARNING: Only {len(measurements)} samples after outlier removal")

            outliers_removed = original_count - len(measurements)

            # Calculate comprehensive statistics
            if not measurements:
                measurements = [1.0]  # Fallback

            min_time = min(measurements)
            mean_time = statistics.mean(measurements)
            max_time = max(measurements)
            std_time = statistics.stdev(measurements) if len(measurements) > 1 else 0.0
            noise_ratio = std_time / mean_time if mean_time > 0 else 0.0
            ops_per_sec = 1_000_000_000 / mean_time if mean_time > 0 else 0.0

            self._result = BenchmarkResult(
                name=self.prefix,
                description=func.__doc__.strip() if func.__doc__ else "No description",
                min_ns=min_time,
                mean_ns=mean_time,
                max_ns=max_time,
                std_ns=std_time,
                samples=len(measurements),
                noise_ratio=noise_ratio,
                ops_per_sec=ops_per_sec,
            )

            # Enhanced status reporting
            status_parts = [
                f"{self._result.stability_grade}",
                f"{len(measurements)} samples",
                f"{measurement_type} method",
            ]

            if outliers_removed > 0:
                status_parts.append(f"{outliers_removed} outliers removed")

            status = f" ({', '.join(status_parts)})"
            print(f"\r    :: BENCHMARKING {self.prefix} PASSED{status}")

    @property
    def result(self) -> Optional[BenchmarkResult]:
        """Get benchmark result"""
        return self._result


class BenchmarkCase:
    """Individual benchmark case"""

    __slots__ = ("func", "name", "_fixtures", "_results")

    def __init__(self, func: Callable, name: str):
        self.func = func
        self.name = name
        self._fixtures = [
            _registered_fixtures[name]
            for name in inspect.signature(func).parameters.keys()
            if name != "ctx"
        ]
        self._results: List[BenchmarkResult] = []

    def _call_with_fixtures(self, params: List[FixtureResult]):
        """Execute benchmark with specific fixture parameters"""
        ctx = Context(tuple(i.id for i in params))
        params_values = tuple(i.result for i in params)

        try:
            self.func(ctx, *params_values)
            if ctx.result:
                self._results.append(ctx.result)
        except SkipError:
            print(f"    :: SKIPPED {ctx.prefix}")
        except Exception as e:
            import traceback

            traceback.print_exception(e)
            print(f"    :: ERROR {ctx.prefix}: {e}")

    def _iter_fixture(self, params: List[FixtureResult] = []):
        """Iterate through all fixture combinations"""
        if not self._fixtures:
            return self._call_with_fixtures(params)

        index = len(params)
        if index >= len(self._fixtures):
            return self._call_with_fixtures(params)

        for obj in self._fixtures[index]:
            self._iter_fixture(params + [obj])

    def run(self):
        """Run all fixture combinations for this benchmark"""
        self._iter_fixture()

    @property
    def results(self) -> List[BenchmarkResult]:
        """Get all results for this benchmark case"""
        return self._results


def benchmark(name: Optional[str] = None):
    """Decorator to register a benchmark function"""

    def __inner(func):
        case = BenchmarkCase(func, name or func.__name__)
        _registered_cases.append(case)
        return func

    return __inner


def run_benchmarks(specific: str = ""):
    """Run all registered benchmarks"""
    print("=" * 80)
    print("OPTIMIZED BENCHMARK SUITE")
    print("=" * 80)
    print(f"Timer Resolution: {_TIMER.resolution_ns:.1f}ns")
    print(f"Timer Overhead: {_TIMER.overhead_ns:.1f}ns")
    print(f"Target Measurement Time: {TARGET_TOTAL_TIME_NS / 1_000_000:.0f}ms")
    print(f"Minimum Samples: {MIN_SAMPLES}")
    print("=" * 80)
    print()

    if specific:
        cases = [case for case in _registered_cases if specific in case.name]
    else:
        cases = _registered_cases

    for case in cases:
        print(f":: BENCHMARK {case.name}")
        case.run()
        print()

        # Brief pause to let system stabilize
        time.sleep(0.1)

        yield case.name, case.results
