from __future__ import annotations

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.cases.base import Case, fill
from cachebox_benchmark.config import MAXSIZE
from cachebox_benchmark.harness.types import Prepared


def skip_reason(impl: Impl) -> str | None:
    if not impl.has_eviction_policy:
        return "no eviction policy"
    if not impl.supports_popitem or impl.popitem is None:
        return "no popitem"
    return None


def prepare(impl: Impl) -> Prepared:
    popitem = impl.popitem
    assert popitem is not None
    factory = impl.factory

    def probe() -> None:
        cache = factory(16)
        impl.set(cache, 1, 1)
        popitem(cache)

    def setup():
        cache = factory(MAXSIZE)
        fill(impl, cache, 0, MAXSIZE)
        return cache

    def run(cache, loops: int) -> None:
        for _ in range(loops):
            popitem(cache)

    return Prepared(
        setup_each_sample=True,
        setup=setup,
        run=run,
        max_loops=MAXSIZE,
        probe=probe,
    )


CASE = Case(
    name="popitem",
    title="Popitem",
    summary="Call popitem() on a cache filled to maxsize (the eviction primitive).",
    skip_reason=skip_reason,
    prepare=prepare,
)
