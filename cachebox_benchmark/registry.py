from __future__ import annotations

import cachebox
import cacheing
import cachetools
import lru
import moka_py

from cachebox_benchmark.adapters import Impl, mapping, moka_delete, moka_get, moka_set
from cachebox_benchmark.config import TTL_SECONDS


def _moka(maxsize: int):
    return moka_py.Moka(maxsize)


def _moka_lru(maxsize: int):
    return moka_py.Moka(maxsize, policy="lru")


def build_impls() -> tuple[Impl, ...]:
    return (
        mapping(
            id="dict",
            family="stdlib",
            factory=lambda _n: {},
            bounded=False,
            has_eviction_policy=False,
            supports_popitem=False,
        ),
        mapping(
            id="cachebox.Cache",
            family="cachebox",
            factory=lambda n: cachebox.Cache(n),
            bounded=True,
            has_eviction_policy=False,
            supports_popitem=False,
        ),
        mapping(
            id="cachetools.Cache",
            family="cachetools",
            factory=lambda n: cachetools.Cache(n),
            bounded=True,
            has_eviction_policy=False,
            supports_popitem=False,
        ),
        mapping(
            id="cachebox.FIFOCache",
            family="cachebox",
            factory=lambda n: cachebox.FIFOCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachetools.FIFOCache",
            family="cachetools",
            factory=lambda n: cachetools.FIFOCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachebox.LRUCache",
            family="cachebox",
            factory=lambda n: cachebox.LRUCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachetools.LRUCache",
            family="cachetools",
            factory=lambda n: cachetools.LRUCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="lru.LRU",
            family="lru-dict",
            factory=lambda n: lru.LRU(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cacheing.LRUCache",
            family="cacheing",
            factory=lambda n: cacheing.LRUCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachebox.LFUCache",
            family="cachebox",
            factory=lambda n: cachebox.LFUCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cacheing.LFUCache",
            family="cacheing",
            factory=lambda n: cacheing.LFUCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachetools.LFUCache",
            family="cachetools",
            factory=lambda n: cachetools.LFUCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachebox.RRCache",
            family="cachebox",
            factory=lambda n: cachebox.RRCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cacheing.RandomCache",
            family="cacheing",
            factory=lambda n: cacheing.RandomCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachetools.RRCache",
            family="cachetools",
            factory=lambda n: cachetools.RRCache(n),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachebox.TTLCache",
            family="cachebox",
            factory=lambda n: cachebox.TTLCache(n, TTL_SECONDS),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachetools.TTLCache",
            family="cachetools",
            factory=lambda n: cachetools.TTLCache(n, TTL_SECONDS),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cacheing.TTLCache",
            family="cacheing",
            factory=lambda n: cacheing.TTLCache(n, TTL_SECONDS),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        mapping(
            id="cachebox.VTTLCache",
            family="cachebox",
            factory=lambda n: cachebox.VTTLCache(n, ttl=TTL_SECONDS),
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=True,
        ),
        Impl(
            id="moka_py.Moka",
            family="moka",
            factory=_moka,
            set=moka_set,
            get=moka_get,
            delete=moka_delete,
            popitem=None,
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=False,
        ),
        Impl(
            id="moka_py.Moka (lru)",
            family="moka",
            factory=_moka_lru,
            set=moka_set,
            get=moka_get,
            delete=moka_delete,
            popitem=None,
            bounded=True,
            has_eviction_policy=True,
            supports_popitem=False,
        ),
    )


IMPLS: tuple[Impl, ...] = build_impls()
IMPL_BY_ID: dict[str, Impl] = {impl.id: impl for impl in IMPLS}
