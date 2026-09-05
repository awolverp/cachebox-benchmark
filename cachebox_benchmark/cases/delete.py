from __future__ import annotations

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.cases.base import Case, fill
from cachebox_benchmark.config import MAXSIZE
from cachebox_benchmark.harness.types import Prepared, ProbeError


def skip_reason(_impl: Impl) -> str | None:
    return None


def prepare(impl: Impl) -> Prepared:
    delete = impl.delete
    factory = impl.factory

    def probe() -> None:
        cache = factory(16)
        impl.set(cache, 1, 1)
        delete(cache, 1)
        if impl.get(cache, 1) is not None:
            raise ProbeError("delete did not remove key")

    def setup():
        cache = factory(MAXSIZE)
        fill(impl, cache, 0, MAXSIZE)
        return cache

    def run(cache, loops: int) -> None:
        for i in range(loops):
            delete(cache, i)

    return Prepared(
        setup_each_sample=True,
        setup=setup,
        run=run,
        max_loops=MAXSIZE,
        probe=probe,
    )


CASE = Case(
    name="delete",
    title="Deletion",
    summary="Delete keys that exist. Each sample populates maxsize entries and deletes them once.",
    skip_reason=skip_reason,
    prepare=prepare,
)
