from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from cachebox_benchmark.adapters import Impl
from cachebox_benchmark.config import MAXSIZE, SET_NEW_FILL_RATIO, SET_NEW_HEADROOM_RATIO
from cachebox_benchmark.harness.types import Prepared


@dataclass(frozen=True)
class Case:
    name: str
    title: str
    summary: str
    skip_reason: Callable[[Impl], str | None]
    prepare: Callable[[Impl], Prepared]


def fill(impl: Impl, cache: Any, start: int, count: int) -> None:
    set_ = impl.set
    for i in range(start, start + count):
        set_(cache, i, i)


def set_new_fill_count() -> int:
    return int(MAXSIZE * SET_NEW_FILL_RATIO)


def set_new_max_loops(impl: Impl) -> int | None:
    fill_count = set_new_fill_count()
    if not impl.bounded:
        return None
    if impl.has_eviction_policy:
        headroom = int(MAXSIZE * SET_NEW_HEADROOM_RATIO)
        return max(1, headroom - fill_count)
    return max(1, MAXSIZE - fill_count)
