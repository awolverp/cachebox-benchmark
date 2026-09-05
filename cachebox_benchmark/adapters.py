from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

Factory = Callable[[int], Any]
Ternary = Callable[[Any, Any, Any], None]
BinaryGet = Callable[[Any, Any], Any]
BinaryDel = Callable[[Any, Any], None]
Unary = Callable[[Any], Any]


@dataclass(frozen=True)
class Impl:
    id: str
    family: str
    factory: Factory
    set: Ternary
    get: BinaryGet
    delete: BinaryDel
    popitem: Unary | None
    bounded: bool
    has_eviction_policy: bool
    supports_popitem: bool


def mapping_set(cache: Any, key: Any, value: Any) -> None:
    cache[key] = value


def mapping_get(cache: Any, key: Any) -> Any:
    return cache.get(key, None)


def mapping_delete(cache: Any, key: Any) -> None:
    del cache[key]


def mapping_popitem(cache: Any) -> Any:
    return cache.popitem()


def moka_set(cache: Any, key: Any, value: Any) -> None:
    cache.set(key, value)


def moka_get(cache: Any, key: Any) -> Any:
    return cache.get(key, None)


def moka_delete(cache: Any, key: Any) -> None:
    cache.remove(key)


def mapping(
    *,
    id: str,
    family: str,
    factory: Factory,
    bounded: bool,
    has_eviction_policy: bool,
    supports_popitem: bool,
) -> Impl:
    return Impl(
        id=id,
        family=family,
        factory=factory,
        set=mapping_set,
        get=mapping_get,
        delete=mapping_delete,
        popitem=mapping_popitem if supports_popitem else None,
        bounded=bounded,
        has_eviction_policy=has_eviction_policy,
        supports_popitem=supports_popitem,
    )
