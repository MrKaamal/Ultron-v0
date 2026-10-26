from __future__ import annotations


def run_react_loop(prompt: str, offline: bool = True) -> str:
    mode = "offline" if offline else "online"
    return f"[ultron-brain:{mode}] {prompt}"
