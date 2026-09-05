from __future__ import annotations

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.cases.base import Case, fill
from cachebox_benchmark.config import MAXSIZE
from cachebox_benchmark.harness.types import Prepared


def skip_reason(impl: Impl) -> str | None:
    if not impl.has_eviction_policy:
        return "no eviction policy"
    return None


def prepare(impl: Impl) -> Prepared:
    set_ = impl.set
    factory = impl.factory

    def setup():
        cache = factory(MAXSIZE)
        fill(impl, cache, 0, MAXSIZE)
        return cache

    def run(cache, loops: int) -> None:
        base = MAXSIZE
        for i in range(loops):
            key = base + i
            set_(cache, key, key)

    return Prepared(
        setup_each_sample=True,
        setup=setup,
        run=run,
        max_loops=MAXSIZE,
    )


CASE = Case(
    name="set_evict",
    title="Set at capacity (eviction)",
    summary="Insert new keys into a cache already at maxsize so each set evicts an entry.",
    skip_reason=skip_reason,
    prepare=prepare,
)
