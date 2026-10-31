from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from cachebox_benchmark.harness.stats import Stats


class ProbeError(Exception):
    pass


@dataclass
class Prepared:
    setup_each_sample: bool
    setup: Callable[[], Any]
    run: Callable[[Any, int], None]
    teardown: Callable[[Any], None] | None = None
    max_loops: int | None = None
    probe: Callable[[], None] | None = None
    min_loops: int | None = None


@dataclass
class BenchmarkResult:
    case: str
    impl: str
    skipped: bool
    skip_reason: str | None = None
    stats: Stats | None = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "case": self.case,
            "impl": self.impl,
            "skipped": self.skipped,
            "skip_reason": self.skip_reason,
            "warnings": list(self.warnings),
        }
        if self.stats is not None:
            payload["stats"] = self.stats.to_dict()
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BenchmarkResult:
        stats = None
        if data.get("stats") is not None:
            stats = Stats.from_dict(data["stats"])
        return cls(
            case=data["case"],
            impl=data["impl"],
            skipped=bool(data.get("skipped")),
            skip_reason=data.get("skip_reason"),
            stats=stats,
            warnings=list(data.get("warnings") or []),
        )
