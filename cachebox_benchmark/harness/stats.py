from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Stats:
    samples: list[float]
    loops: int
    mean_ns: float
    median_ns: float
    stdev_ns: float
    mad_ns: float
    min_ns: float
    max_ns: float
    p95_ns: float
    ops_per_sec: float
    cv: float
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "samples": list(self.samples),
            "loops": self.loops,
            "mean_ns": self.mean_ns,
            "median_ns": self.median_ns,
            "stdev_ns": self.stdev_ns,
            "mad_ns": self.mad_ns,
            "min_ns": self.min_ns,
            "max_ns": self.max_ns,
            "p95_ns": self.p95_ns,
            "ops_per_sec": self.ops_per_sec,
            "cv": self.cv,
            "warnings": list(self.warnings),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Stats:
        return cls(
            samples=list(data["samples"]),
            loops=int(data["loops"]),
            mean_ns=float(data["mean_ns"]),
            median_ns=float(data["median_ns"]),
            stdev_ns=float(data["stdev_ns"]),
            mad_ns=float(data["mad_ns"]),
            min_ns=float(data["min_ns"]),
            max_ns=float(data["max_ns"]),
            p95_ns=float(data["p95_ns"]),
            ops_per_sec=float(data["ops_per_sec"]),
            cv=float(data["cv"]),
            warnings=list(data.get("warnings") or []),
        )


def _percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * p
    lo = int(math.floor(k))
    hi = int(math.ceil(k))
    if lo == hi:
        return sorted_vals[lo]
    weight = k - lo
    return sorted_vals[lo] * (1.0 - weight) + sorted_vals[hi] * weight


def summarize(samples: list[float], loops: int) -> Stats:
    if not samples:
        samples = [1.0]
    mean = statistics.mean(samples)
    median = statistics.median(samples)
    stdev = statistics.stdev(samples) if len(samples) > 1 else 0.0
    mad = statistics.median([abs(x - median) for x in samples])
    cv = (stdev / mean) if mean > 0 else 0.0
    ordered = sorted(samples)
    warnings: list[str] = []
    if cv > 0.10:
        warnings.append(
            f"the standard deviation ({stdev:.1f} ns) is {cv:.0%} of the mean ({mean:.1f} ns)"
        )
    if mean > 0 and max(samples) > 1.5 * mean:
        pct = (max(samples) / mean - 1.0) * 100.0
        warnings.append(
            f"the maximum ({max(samples):.1f} ns) is {pct:.0f}% greater than the mean ({mean:.1f} ns)"
        )
    return Stats(
        samples=list(samples),
        loops=loops,
        mean_ns=mean,
        median_ns=median,
        stdev_ns=stdev,
        mad_ns=mad,
        min_ns=min(samples),
        max_ns=max(samples),
        p95_ns=_percentile(ordered, 0.95),
        ops_per_sec=(1_000_000_000.0 / mean) if mean > 0 else 0.0,
        cv=cv,
        warnings=warnings,
    )
