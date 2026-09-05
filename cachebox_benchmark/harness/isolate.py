from __future__ import annotations

import json
import os
import subprocess
import sys

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.config import RunConfig
from cachebox_benchmark.harness.types import BenchmarkResult


def run_isolated(
    *,
    case_name: str,
    impl: Impl,
    config: RunConfig,
) -> BenchmarkResult:
    cmd = [
        sys.executable,
        "-m",
        "cachebox_benchmark",
        "--worker",
        "--case",
        case_name,
        "--impl",
        impl.id,
        "--samples",
        str(config.samples),
        "--warmup",
        str(config.warmup),
        "--min-time",
        str(config.min_time_ns / 1_000_000_000),
    ]
    if config.fast:
        cmd.append("--fast")
    if config.nice:
        cmd.append("--nice")
    if config.pin_cpu is not None:
        cmd.extend(["--pin-cpu", str(config.pin_cpu)])

    env = os.environ.copy()
    if case_name != "collision":
        env["PYTHONHASHSEED"] = config.hash_seed

    proc = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    if proc.stderr:
        sys.stderr.write(proc.stderr)
        if not proc.stderr.endswith("\n"):
            sys.stderr.write("\n")
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason=f"worker failed: {err[-400:]}",
        )
    line = (proc.stdout or "").strip().splitlines()
    if not line:
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason="worker produced no JSON",
        )
    try:
        return BenchmarkResult.from_dict(json.loads(line[-1]))
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        return BenchmarkResult(
            case=case_name,
            impl=impl.id,
            skipped=True,
            skip_reason=f"worker JSON error: {exc}",
        )
