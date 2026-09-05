from __future__ import annotations

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.cases.base import Case
from cachebox_benchmark.config import COLLISION_KEYS, MAXSIZE
from cachebox_benchmark.harness.types import Prepared, ProbeError


class BadHash(int):
    def __hash__(self) -> int:
        return 42


def skip_reason(_impl: Impl) -> str | None:
    return None


def prepare(impl: Impl) -> Prepared:
    get = impl.get
    set_ = impl.set
    factory = impl.factory
    keys = [BadHash(i) for i in range(COLLISION_KEYS)]

    def setup():
        cache = factory(MAXSIZE)
        for key in keys:
            set_(cache, key, int(key))
        present = [key for key in keys if get(cache, key) is not None]
        if not present:
            raise ProbeError("no colliding keys present after populate")
        return cache, present

    def run(state, loops: int) -> None:
        cache, present = state
        n = len(present)
        for i in range(loops):
            get(cache, present[i % n])

    return Prepared(
        setup_each_sample=False,
        setup=setup,
        run=run,
        max_loops=None,
    )


CASE = Case(
    name="collision",
    title="Hash collision",
    summary="Look up keys that all hash to the same value (hash() == 42).",
    skip_reason=skip_reason,
    prepare=prepare,
)
