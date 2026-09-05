from __future__ import annotations

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.cases.base import Case, fill, set_new_fill_count, set_new_max_loops
from cachebox_benchmark.config import MAXSIZE
from cachebox_benchmark.harness.types import Prepared


def skip_reason(_impl: Impl) -> str | None:
    return None


def prepare(impl: Impl) -> Prepared:
    fill_count = set_new_fill_count()
    set_ = impl.set
    factory = impl.factory
    max_loops = set_new_max_loops(impl)

    def setup():
        cache = factory(MAXSIZE)
        fill(impl, cache, 0, fill_count)
        return cache

    def run(cache, loops: int) -> None:
        base = fill_count
        for i in range(loops):
            key = base + i
            set_(cache, key, key)

    return Prepared(
        setup_each_sample=True,
        setup=setup,
        run=run,
        max_loops=max_loops,
    )


CASE = Case(
    name="set_new",
    title="Set new (no eviction)",
    summary="Insert keys that do not exist and do not trigger eviction. Cache is pre-filled to 25% of maxsize.",
    skip_reason=skip_reason,
    prepare=prepare,
)
