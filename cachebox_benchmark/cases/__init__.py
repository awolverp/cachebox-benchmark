from __future__ import annotations

from cachebox_benchmark.cases.base import Case
from cachebox_benchmark.cases.collision import CASE as collision
from cachebox_benchmark.cases.delete import CASE as delete
from cachebox_benchmark.cases.get_hit import CASE as get_hit
from cachebox_benchmark.cases.get_miss import CASE as get_miss
from cachebox_benchmark.cases.popitem import CASE as popitem
from cachebox_benchmark.cases.set_evict import CASE as set_evict
from cachebox_benchmark.cases.set_new import CASE as set_new

CASES: tuple[Case, ...] = (
    set_new,
    set_evict,
    get_hit,
    get_miss,
    delete,
    popitem,
    collision,
)
CASE_BY_NAME: dict[str, Case] = {case.name: case for case in CASES}


def resolve_cases(names: list[str] | None) -> list[Case]:
    if not names:
        return list(CASES)
    unknown = [name for name in names if name not in CASE_BY_NAME]
    if unknown:
        known = ", ".join(CASE_BY_NAME)
        raise SystemExit(f"unknown case(s): {', '.join(unknown)}\nknown: {known}")
    return [CASE_BY_NAME[name] for name in names]
