from __future__ import annotations

from pathlib import Path
from typing import Any

from cachebox_benchmark.cases import CASE_BY_NAME, CASES
from cachebox_benchmark.harness.types import BenchmarkResult
from cachebox_benchmark.report.meta import format_system_info

_TEMPLATE = Path(__file__).with_name("template.md")


def _fmt_ns(value: float) -> str:
    return f"{value:,.1f}"


def _fmt_ops(ops: float) -> str:
    return f"{ops / 1e6:.1f}M"


def _table(results: list[BenchmarkResult]) -> str:
    rows = [
        "| Implementation | Median (ns) | Mean (ns) | Stdev | MAD | Ops/sec | Samples | CV |",
        "| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    ranked = sorted(
        (r for r in results if not r.skipped and r.stats is not None),
        key=lambda r: r.stats.median_ns,  # type: ignore[union-attr]
    )
    for result in ranked:
        stats = result.stats
        assert stats is not None
        rows.append(
            "| "
            + " | ".join(
                [
                    result.impl,
                    _fmt_ns(stats.median_ns),
                    _fmt_ns(stats.mean_ns),
                    _fmt_ns(stats.stdev_ns),
                    _fmt_ns(stats.mad_ns),
                    _fmt_ops(stats.ops_per_sec),
                    str(len(stats.samples)),
                    f"{stats.cv * 100:.1f}%",
                ]
            )
            + " |"
        )
    skipped = [r for r in results if r.skipped]
    if skipped:
        rows.append("")
        rows.append("Skipped: " + ", ".join(f"`{r.impl}` ({r.skip_reason})" for r in skipped))
    return "\n".join(rows)


def _results_markdown(results: list[BenchmarkResult]) -> str:
    by_case: dict[str, list[BenchmarkResult]] = {}
    for result in results:
        by_case.setdefault(result.case, []).append(result)

    parts: list[str] = []
    order = [case.name for case in CASES if case.name in by_case]
    order.extend(name for name in by_case if name not in order)
    for case_name in order:
        case_results = by_case[case_name]
        timed = [r for r in case_results if not r.skipped and r.stats is not None]
        title = CASE_BY_NAME[case_name].title if case_name in CASE_BY_NAME else case_name
        summary = CASE_BY_NAME[case_name].summary if case_name in CASE_BY_NAME else ""
        parts.append(f"## 📊 {title}")
        parts.append("")
        if summary:
            parts.append(summary)
            parts.append("")
        parts.append(f"![{case_name}](photos/{case_name}.png)")
        parts.append("")
        if timed:
            fastest = min(timed, key=lambda r: r.stats.median_ns)  # type: ignore[union-attr]
            slowest = max(timed, key=lambda r: r.stats.median_ns)  # type: ignore[union-attr]
            assert fastest.stats is not None and slowest.stats is not None
            span = (
                slowest.stats.median_ns / fastest.stats.median_ns
                if fastest.stats.median_ns
                else 0.0
            )
            parts.append(
                f"- **Range**: {span:.1f}× between fastest and slowest (median)\n"
                f"- **Best**: {fastest.impl} "
                f"({fastest.stats.median_ns:.0f} ns, {fastest.stats.ops_per_sec / 1e6:.1f}M ops/sec)\n"
            )
        parts.append(_table(case_results))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_readme(
    results: list[BenchmarkResult],
    metadata: dict[str, Any],
) -> str:
    template = _TEMPLATE.read_text(encoding="utf-8")
    banner = ""
    if metadata.get("fast"):
        banner = (
            "> **Note:** These results used `--fast` (shorter samples). "
            "Re-run without `--fast` for publishable numbers.\n"
        )
    text = template.replace("{{FAST_BANNER}}", banner)
    text = text.replace("{{SYSTEM_INFO}}", format_system_info(metadata))
    text = text.replace("{{RESULTS}}", _results_markdown(results))
    return text


def write_readme(
    path: Path,
    results: list[BenchmarkResult],
    metadata: dict[str, Any],
) -> None:
    text = render_readme(results, metadata)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
