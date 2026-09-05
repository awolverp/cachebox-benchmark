from __future__ import annotations

from dataclasses import dataclass

MAXSIZE = 4096
TTL_SECONDS = 3600.0
SET_NEW_FILL_RATIO = 0.25
SET_NEW_HEADROOM_RATIO = 0.90
COLLISION_KEYS = 256

DEFAULT_MIN_TIME_NS = 100_000_000  # 100 ms, pyperf default
FAST_MIN_TIME_NS = 10_000_000  # 10 ms
DEFAULT_SAMPLES = 25
FAST_SAMPLES = 5
DEFAULT_WARMUP = 1
MAX_SAMPLES = 200


@dataclass(frozen=True)
class RunConfig:
    min_time_ns: int = DEFAULT_MIN_TIME_NS
    warmup: int = DEFAULT_WARMUP
    samples: int = DEFAULT_SAMPLES
    isolated: bool = False
    pin_cpu: int | None = None
    nice: bool = False
    fast: bool = False
    hash_seed: str = "0"

    @classmethod
    def from_flags(
        cls,
        *,
        fast: bool = False,
        isolated: bool = False,
        pin_cpu: int | None = None,
        nice: bool = False,
        min_time: float | None = None,
        samples: int | None = None,
        warmup: int | None = None,
    ) -> RunConfig:
        min_time_ns = DEFAULT_MIN_TIME_NS
        n_samples = DEFAULT_SAMPLES
        if fast:
            min_time_ns = FAST_MIN_TIME_NS
            n_samples = FAST_SAMPLES
        if min_time is not None:
            min_time_ns = max(1, int(min_time * 1_000_000_000))
        if samples is not None:
            n_samples = max(1, samples)
        return cls(
            min_time_ns=min_time_ns,
            warmup=DEFAULT_WARMUP if warmup is None else max(0, warmup),
            samples=n_samples,
            isolated=isolated,
            pin_cpu=pin_cpu,
            nice=nice,
            fast=fast,
        )
