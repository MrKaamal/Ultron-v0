from __future__ import annotations

from dataclasses import dataclass
from time import time


@dataclass(slots=True)
class Heartbeat:
    node_id: str
    timestamp: float
    status: str = "online"


def make_heartbeat(node_id: str) -> Heartbeat:
    return Heartbeat(node_id=node_id, timestamp=time())
