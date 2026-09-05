from __future__ import annotations

import gc
import os
import platform
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from cachebox_benchmark.config import RunConfig
from cachebox_benchmark.harness.timer import Timer

_VERSION_PACKAGES = (
    "cachebox",
    "cachetools",
    "cacheing",
    "lru-dict",
    "moka-py",
    "matplotlib",
    "matplotx",
)


def cpu_model() -> str:
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    return platform.processor() or platform.machine()


def package_versions() -> dict[str, str]:
    import importlib.metadata as metadata

    versions: dict[str, str] = {}
    for name in _VERSION_PACKAGES:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "unknown"
    return versions


def collect_metadata(config: RunConfig, timer: Timer) -> dict[str, object]:
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "processor": cpu_model(),
        "libraries": package_versions(),
        "timer_resolution_ns": timer.resolution_ns,
        "timer_overhead_ns": timer.overhead_ns,
        "min_time_ns": config.min_time_ns,
        "warmup": config.warmup,
        "samples": config.samples,
        "isolated": config.isolated,
        "fast": config.fast,
        "pin_cpu": config.pin_cpu,
        "nice": config.nice,
        "hash_seed": os.environ.get("PYTHONHASHSEED", "unset"),
        "gc_disabled_during_measure": True,
        "threaded": False,
    }


@contextmanager
def applied_host_policy(config: RunConfig) -> Iterator[None]:
    original_nice = None
    original_affinity = None
    process = None

    if config.nice:
        try:
            original_nice = os.nice(0)
            os.nice(-10 - original_nice)
        except (OSError, PermissionError):
            original_nice = None

    if config.pin_cpu is not None:
        try:
            import psutil

            process = psutil.Process()
            original_affinity = process.cpu_affinity()
            process.cpu_affinity([config.pin_cpu])
        except (ImportError, AttributeError, OSError, PermissionError):
            original_affinity = None
            process = None

    try:
        yield
    finally:
        if original_affinity is not None and process is not None:
            try:
                process.cpu_affinity(original_affinity)
            except (OSError, PermissionError):
                pass
        if original_nice is not None:
            try:
                current = os.nice(0)
                os.nice(original_nice - current)
            except (OSError, PermissionError):
                pass


def warmup_cpu(seconds: float = 0.25) -> None:
    import math
    import time

    end = time.perf_counter() + seconds
    i = 0
    while time.perf_counter() < end:
        math.sqrt(i)
        i += 1


def gc_pause() -> None:
    gc.collect()
    gc.disable()


def gc_resume() -> None:
    if not gc.isenabled():
        gc.enable()
