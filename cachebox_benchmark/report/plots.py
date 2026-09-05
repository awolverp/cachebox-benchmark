from __future__ import annotations

from pathlib import Path

from cachebox_benchmark.cases import CASE_BY_NAME
from cachebox_benchmark.harness.types import BenchmarkResult


def write_plots(
    results: list[BenchmarkResult],
    photos_dir: Path,
) -> dict[str, Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotx

    photos_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    by_case: dict[str, list[BenchmarkResult]] = {}
    for result in results:
        if result.skipped or result.stats is None:
            continue
        by_case.setdefault(result.case, []).append(result)

    for case_name, case_results in by_case.items():
        case_results = sorted(case_results, key=lambda r: r.stats.median_ns)  # type: ignore[union-attr]
        labels = [r.impl for r in case_results]
        medians = [r.stats.median_ns for r in case_results]  # type: ignore[union-attr]
        stds = [r.stats.stdev_ns for r in case_results]  # type: ignore[union-attr]
        ops = [r.stats.ops_per_sec / 1e6 for r in case_results]  # type: ignore[union-attr]
        title = CASE_BY_NAME[case_name].title if case_name in CASE_BY_NAME else case_name

        try:
            style_ctx = matplotx.styles.aura["dark"]
        except Exception:
            style_ctx = "seaborn-v0_8-darkgrid"

        with plt.style.context(style_ctx):
            fig, ax = plt.subplots(figsize=(14, 7))
            x = range(len(labels))
            bars = ax.bar(
                x,
                medians,
                yerr=stds,
                capsize=6,
                linewidth=0.8,
                edgecolor="#222222",
                color="#1762A4",
                alpha=0.95,
            )
            ax.set_yscale("log")
            ax.set_xticks(list(x))
            ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=11)
            ax.set_ylabel("Median time (ns) — log scale", fontsize=12)
            ax.set_title(title, fontsize=16, fontweight="bold", pad=12)
            ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
            for rect, median in zip(bars, medians):
                height = rect.get_height()
                ax.text(
                    rect.get_x() + rect.get_width() / 2,
                    height * 1.18 if height else 1.0,
                    f"{int(median):,} ns",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    color="black",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85),
                )
            ax2 = ax.twinx()
            ax2.plot(
                list(x),
                ops,
                marker="o",
                linestyle="-",
                linewidth=2,
                markersize=6,
                color="#3498DB",
            )
            ax2.set_ylabel("Throughput (Mops/sec)", fontsize=12)
            ax2.set_ylim(bottom=0)
            for xi, opm in zip(x, ops):
                ax2.text(xi, opm, f"{opm:.2f}M", ha="center", va="bottom", fontsize=9)
            fig.tight_layout()
            out = photos_dir / f"{case_name}.png"
            fig.savefig(out, dpi=250, bbox_inches="tight")
            plt.close(fig)
            written[case_name] = out
    return written
