from __future__ import annotations

import argparse

from src.cognition.ultron_brain import run_react_loop


def main() -> None:
    parser = argparse.ArgumentParser(description="Ultron Sovereign Orchestrator")
    parser.add_argument("--offline", action="store_true", help="Run in offline mode")
    parser.add_argument("prompt", nargs="?", default="System initialized.")
    args = parser.parse_args()

    print(run_react_loop(args.prompt, offline=args.offline))


if __name__ == "__main__":
    main()
