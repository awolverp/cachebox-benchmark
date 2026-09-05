from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from cachebox_benchmark.cases import CASE_BY_NAME, CASES, resolve_cases
from cachebox_benchmark.config import RunConfig
from cachebox_benchmark.harness.env import (
    applied_host_policy,
    collect_metadata,
    warmup_cpu,
)
from cachebox_benchmark.harness.isolate import run_isolated
from cachebox_benchmark.harness.runner import format_result, measure
from cachebox_benchmark.harness.timer import Timer
from cachebox_benchmark.harness.types import BenchmarkResult
from cachebox_benchmark.registry import IMPL_BY_ID, IMPLS


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cachebox-benchmark",
        description="Compare Python cache libraries with a pyperf-style micro-benchmark harness.",
    )
    parser.add_argument(
        "cases",
        nargs="*",
        help="Case names (default: all). Known: " + ", ".join(c.name for c in CASES),
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Shorter samples; not for published numbers.",
    )
    parser.add_argument(
        "--isolated",
        action="store_true",
        help="Run each (case, impl) in a subprocess.",
    )
    parser.add_argument("--json", type=Path, help="Write results JSON to this path.")
    parser.add_argument(
        "--report-only",
        type=Path,
        help="Skip timing; generate plots and README from a JSON file.",
    )
    parser.add_argument(
        "--no-report", action="store_true", help="Do not write README.md or photos."
    )
    parser.add_argument(
        "--pin-cpu", type=int, default=None, help="Pin this process to a CPU index."
    )
    parser.add_argument(
        "--nice", action="store_true", help="Raise process priority (os.nice(-10))."
    )
    parser.add_argument(
        "--min-time", type=float, default=None, help="Seconds per sample (default 0.1)."
    )
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--warmup", type=int, default=None)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--case", dest="worker_case", default=None, help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--impl", dest="worker_impl", default=None, help=argparse.SUPPRESS
    )
    return parser


def _dump(path: Path, results: list[BenchmarkResult], metadata: dict[str, Any]) -> None:
    payload = {
        "metadata": metadata,
        "results": [result.to_dict() for result in results],
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def _load(path: Path) -> tuple[list[BenchmarkResult], dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = [BenchmarkResult.from_dict(item) for item in payload["results"]]
    return results, dict(payload.get("metadata") or {})


def _write_report(
    results: list[BenchmarkResult], metadata: dict[str, Any], root: Path
) -> None:
    from cachebox_benchmark.report.markdown import write_readme
    from cachebox_benchmark.report.plots import write_plots

    write_plots(results, root / "photos")
    write_readme(root / "README.md", results, metadata)
    print("Wrote photos/ and README.md", file=sys.stderr)


def _run_one(
    case_name: str, impl_id: str, config: RunConfig, timer: Timer
) -> BenchmarkResult:
    case = CASE_BY_NAME[case_name]
    impl = IMPL_BY_ID[impl_id]
    skip = case.skip_reason(impl)
    if skip:
        return BenchmarkResult(
            case=case.name, impl=impl.id, skipped=True, skip_reason=skip
        )
    prepared = case.prepare(impl)
    return measure(
        case_name=case.name,
        impl=impl,
        prepared=prepared,
        config=config,
        timer=timer,
        skip_reason=None,
    )


def _worker_main(args: argparse.Namespace) -> int:
    if not args.worker_case or not args.worker_impl:
        print("worker requires --case and --impl", file=sys.stderr)
        return 2

    if args.worker_case not in CASE_BY_NAME:
        print(f"unknown case {args.worker_case}", file=sys.stderr)
        return 2

    if args.worker_impl not in IMPL_BY_ID:
        print(f"unknown impl {args.worker_impl}", file=sys.stderr)
        return 2

    config = RunConfig.from_flags(
        fast=args.fast,
        isolated=False,
        pin_cpu=args.pin_cpu,
        nice=args.nice,
        min_time=args.min_time,
        samples=args.samples,
        warmup=args.warmup,
    )
    timer = Timer()
    with applied_host_policy(config):
        result = _run_one(args.worker_case, args.worker_impl, config, timer)

    sys.stdout.write(json.dumps(result.to_dict()))
    sys.stdout.write("\n")
    return 0


def _run_suite(args: argparse.Namespace, root: Path) -> int:
    cases = resolve_cases(args.cases)
    config = RunConfig.from_flags(
        fast=args.fast,
        isolated=args.isolated,
        pin_cpu=args.pin_cpu,
        nice=args.nice,
        min_time=args.min_time,
        samples=args.samples,
        warmup=args.warmup,
    )
    timer = Timer()
    metadata = collect_metadata(config, timer)
    print("=" * 72, file=sys.stderr)
    print("CACHE LIBRARY BENCHMARKS", file=sys.stderr)
    print(
        f"Timer resolution {timer.resolution_ns:.1f} ns, overhead {timer.overhead_ns:.1f} ns",
        file=sys.stderr,
    )
    print(
        f"min-time {config.min_time_ns / 1e6:.0f} ms, warmup {config.warmup}, "
        f"samples {config.samples}, isolated={config.isolated}, fast={config.fast}",
        file=sys.stderr,
    )
    print("=" * 72, file=sys.stderr)

    results: list[BenchmarkResult] = []
    with applied_host_policy(config):
        warmup_cpu(0.25)
        for case in cases:
            print(f"\n:: CASE {case.name}", file=sys.stderr)
            for impl in IMPLS:
                skip = case.skip_reason(impl)
                if skip:
                    result = BenchmarkResult(
                        case=case.name,
                        impl=impl.id,
                        skipped=True,
                        skip_reason=skip,
                    )
                elif config.isolated:
                    result = run_isolated(case_name=case.name, impl=impl, config=config)
                else:
                    result = _run_one(case.name, impl.id, config, timer)
                print(format_result(result), file=sys.stderr)
                results.append(result)

    if args.json:
        _dump(args.json, results, metadata)
        print(f"Wrote {args.json}", file=sys.stderr)

    if not args.no_report:
        _write_report(results, metadata, root)
    return 0


def main(argv: list[str] | None = None) -> None:
    args = _parser().parse_args(argv)
    root = Path.cwd()

    if args.worker:
        raise SystemExit(_worker_main(args))

    if args.report_only:
        results, metadata = _load(args.report_only)
        _write_report(results, metadata, root)
        return

    raise SystemExit(_run_suite(args, root))
