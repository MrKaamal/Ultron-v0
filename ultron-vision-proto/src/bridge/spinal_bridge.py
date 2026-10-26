from __future__ import annotations

import ctypes
from pathlib import Path


def load_spinal_core(dll_path: str | None = None) -> ctypes.CDLL:
    if dll_path is None:
        dll_path = str(Path(__file__).resolve().parents[2] / "build" / "actuator_core.dll")
    return ctypes.CDLL(dll_path)
