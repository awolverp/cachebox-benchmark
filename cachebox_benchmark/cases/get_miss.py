from __future__ import annotations

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.cases.base import Case, fill
from cachebox_benchmark.config import MAXSIZE
from cachebox_benchmark.harness.types import Prepared

_MISS_BASE = MAXSIZE + 10_000


def skip_reason(_impl: Impl) -> str | None:
    return None


def prepare(impl: Impl) -> Prepared:
    get = impl.get
    factory = impl.factory

    def setup():
        cache = factory(MAXSIZE)
        fill(impl, cache, 0, MAXSIZE)
        return cache

    def run(cache, loops: int) -> None:
        for i in range(loops):
            get(cache, _MISS_BASE + (i % MAXSIZE))

    return Prepared(
        setup_each_sample=False,
        setup=setup,
        run=run,
        max_loops=None,
    )


CASE = Case(
    name="get_miss",
    title="Lookup missing",
    summary="Look up keys that are not in a populated cache (mapping.get with default None).",
    skip_reason=skip_reason,
    prepare=prepare,
)
