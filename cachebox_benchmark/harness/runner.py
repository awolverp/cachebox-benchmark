from __future__ import annotations

import math

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.config import MAX_SAMPLES, RunConfig
from cachebox_benchmark.harness.stats import summarize
from cachebox_benchmark.harness.timer import Timer
from cachebox_benchmark.harness.types import BenchmarkResult, Prepared, ProbeError
from cachebox_benchmark.harness.env import gc_pause, gc_resume


def probe_basic(impl: Impl) -> None:
    cache = impl.factory(16)
    impl.set(cache, 1, 42)
    got = impl.get(cache, 1)
    if got != 42:
        raise ProbeError(f"get after set returned {got!r}")
    miss = impl.get(cache, 999_999)
    if miss is not None:
        raise ProbeError(f"missing get returned {miss!r}")


def measure(
    *,
    case_name: str,
    impl: Impl,
    prepared: Prepared,
    config: RunConfig,
    timer: Timer,
    skip_reason: str | None = None,
) -> BenchmarkResult:
    if skip_reason:
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason=skip_reason,
        )

    try:
        probe_basic(impl)
        if prepared.probe is not None:
            prepared.probe()
    except ProbeError as exc:
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason=str(exc),
        )
    except Exception as exc:  # noqa: BLE001 — probe any adapter failure
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason=f"probe failed: {type(exc).__name__}: {exc}",
        )

    state = None
    try:
        if not prepared.setup_each_sample:
            state = prepared.setup()
    except ProbeError as exc:
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason=str(exc),
        )
    except Exception as exc:  # noqa: BLE001
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason=f"setup failed: {type(exc).__name__}: {exc}",
        )

    def one_sample(loops: int) -> float:
        nonlocal state
        if prepared.setup_each_sample:
            state = prepared.setup()
        gc_pause()
        try:
            start = timer.func()
            prepared.run(state, loops)
            end = timer.func()
        finally:
            gc_resume()
            if prepared.setup_each_sample and prepared.teardown is not None:
                prepared.teardown(state)
        elapsed = max(1.0, (end - start) - timer.overhead_ns)
        return elapsed / loops

    try:
        cal_loops = 8
        if prepared.max_loops is not None:
            cal_loops = max(1, min(cal_loops, prepared.max_loops))

        one_sample(cal_loops)
        estimate = max(1.0, one_sample(cal_loops))
        desired = max(1, int(config.min_time_ns / estimate))
        loops = desired
        if prepared.max_loops is not None:
            loops = max(1, min(loops, prepared.max_loops))

        n_samples = config.samples
        if prepared.max_loops is not None and loops < desired:
            scale = desired / max(loops, 1)
            n_samples = min(MAX_SAMPLES, max(n_samples, int(math.ceil(config.samples * scale))))

        for _ in range(config.warmup):
            one_sample(loops)

        values = [one_sample(loops) for _ in range(n_samples)]
    except Exception as exc:  # noqa: BLE001
        if not prepared.setup_each_sample and prepared.teardown is not None and state is not None:
            prepared.teardown(state)
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason=f"measure failed: {type(exc).__name__}: {exc}",
        )

    if not prepared.setup_each_sample and prepared.teardown is not None and state is not None:
        prepared.teardown(state)

    stats = summarize(values, loops)
    return BenchmarkResult(
        case=case_name,
        impl=impl.id,
        skipped=False,
        stats=stats,
        warnings=list(stats.warnings),
    )


def format_result(result: BenchmarkResult) -> str:
    prefix = f":: {result.case}  {result.impl}"
    if result.skipped:
        return f"{prefix}  SKIP  {result.skip_reason}"
    assert result.stats is not None
    stats = result.stats
    warn = f"  WARNING: {'; '.join(stats.warnings)}" if stats.warnings else ""
    return (
        f"{prefix}  {stats.median_ns:.1f} ns/op  "
        f"(median, mean {stats.mean_ns:.1f}, cv {stats.cv:.1%}, "
        f"{len(stats.samples)} samples, {stats.loops} loops){warn}"
    )
