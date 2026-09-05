from __future__ import annotations

import time


class Timer:
    __slots__ = ("func", "overhead_ns", "resolution_ns")

    def __init__(self) -> None:
        self.func = time.perf_counter_ns
        self.overhead_ns = self._measure_overhead()
        self.resolution_ns = self._measure_resolution()

    def _measure_overhead(self) -> float:
        timer = self.func
        for _ in range(100):
            timer()
        measurements = []
        for _ in range(1000):
            start = timer()
            end = timer()
            measurements.append(end - start)
        return float(min(measurements))

    def _measure_resolution(self) -> float:
        timer = self.func
        last = timer()
        for _ in range(10_000):
            now = timer()
            diff = now - last
            if diff > 0:
                return float(diff)
            last = now
        return 1.0
