from __future__ import annotations

from itertools import islice

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.cases.base import Case, fill
from cachebox_benchmark.config import MAXSIZE
from cachebox_benchmark.harness.types import Prepared, ProbeError


def skip_reason(impl: Impl) -> str | None:
    if not hasattr(impl.factory(1), "items"):
        return "no iteration API"
    return None


def prepare(impl: Impl) -> Prepared:
    factory = impl.factory

    def setup():
        cache = factory(MAXSIZE)
        fill(impl, cache, 0, MAXSIZE)
        if len(list(cache.items())) != MAXSIZE:
            raise ProbeError("items() did not return maxsize entries")
        return cache

    def run(cache, loops: int) -> None:
        # One loop is one entry: full passes, then a partial one for the remainder.
        passes, rest = divmod(loops, MAXSIZE)
        for _ in range(passes):
            for _item in cache.items():
                pass
        for _item in islice(cache.items(), rest):
            pass

    return Prepared(
        setup_each_sample=False,
        setup=setup,
        run=run,
        max_loops=None,
        # Calibrate on a full pass: some items() build the whole list up front.
        min_loops=MAXSIZE,
    )


CASE = Case(
    name="iterate",
    title="Iterate items",
    summary="Iterate `cache.items()` over a cache filled to maxsize. Time is per entry; creating the iterator is included in the timing.",
    skip_reason=skip_reason,
    prepare=prepare,
)
