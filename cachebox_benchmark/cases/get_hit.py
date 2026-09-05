from __future__ import annotations

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.cases.base import Case, fill
from cachebox_benchmark.config import MAXSIZE
from cachebox_benchmark.harness.types import ProbeError
from cachebox_benchmark.harness.types import Prepared


def skip_reason(_impl: Impl) -> str | None:
    return None


def prepare(impl: Impl) -> Prepared:
    get = impl.get
    factory = impl.factory
    set_ = impl.set

    def setup():
        cache = factory(MAXSIZE)
        fill(impl, cache, 0, MAXSIZE)
        # TinyLFU-style admission may drop a first insert; touch twice.
        for i in range(MAXSIZE):
            set_(cache, i, i)
        keys = [i for i in range(MAXSIZE) if get(cache, i) is not None]
        if not keys:
            raise ProbeError("no keys present after populate")
        return cache, keys

    def run(state, loops: int) -> None:
        cache, keys = state
        n = len(keys)
        for i in range(loops):
            get(cache, keys[i % n])

    return Prepared(
        setup_each_sample=False,
        setup=setup,
        run=run,
        max_loops=None,
    )


CASE = Case(
    name="get_hit",
    title="Lookup existing",
    summary="Look up keys that are in the cache. LRU/LFU recency or frequency updates are part of the API cost.",
    skip_reason=skip_reason,
    prepare=prepare,
)
