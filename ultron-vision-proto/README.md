# ultron-vision-proto

Prototype scaffold for a sovereign multi-layer robotics cognition stack.

## Structure

- `src/spinal_cord/actuator_core.c` — Layer 5 & 6 control/physics core scaffold
- `src/bridge/spinal_bridge.py` — Layer 2 ctypes bridge scaffold
- `src/memory/engram_store.py` — Layer 3 SQLite episodic memory scaffold
- `src/swarm/hive_telemetry.py` — Layer 1 telemetry heartbeat monitor scaffold
- `src/cognition/ultron_brain.py` — Layer 3 ReAct loop scaffold
- `main.py` — Sovereign orchestrator CLI entrypoint

## Quick start

```bash
python main.py --offline
```
