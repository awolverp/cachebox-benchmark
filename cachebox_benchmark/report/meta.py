from __future__ import annotations

from typing import Any


def format_system_info(metadata: dict[str, Any]) -> str:
    libraries = metadata.get("libraries") or {}
    lib_lines = "\n".join(f"  - {name}: {version}" for name, version in libraries.items())
    isolated = "yes" if metadata.get("isolated") else "no"
    fast = "yes" if metadata.get("fast") else "no"
    pin = metadata.get("pin_cpu")
    pin_s = "off" if pin is None else str(pin)
    min_time_ns = float(metadata.get("min_time_ns") or 0)
    min_time = f"{min_time_ns / 1e6:.0f} ms/sample" if min_time_ns else "n/a"
    res = metadata.get("timer_resolution_ns", "?")
    overhead = metadata.get("timer_overhead_ns", "?")
    try:
        res = f"{float(res):.1f}"
        overhead = f"{float(overhead):.1f}"
    except (TypeError, ValueError):
        pass
    return f"""- **Platform**: {metadata.get("platform", "unknown")}
- **Python**: {metadata.get("python", "unknown")}
- **Processor**: {metadata.get("processor", "unknown")}
- **Timer**: resolution {res} ns, overhead {overhead} ns
- **Run**: min-time {min_time}, warmup {metadata.get("warmup", "?")}, samples {metadata.get("samples", "?")}, isolated={isolated}, fast={fast}, pin-cpu={pin_s}, nice={metadata.get("nice", False)}
- **Hash seed**: {metadata.get("hash_seed", "unset")} (isolated workers use 0 except the collision case)
- **GC**: disabled during the timed loop; collected before each sample
- **Threading**: single-threaded (including moka-py)
- **Libraries**:
{lib_lines}"""
