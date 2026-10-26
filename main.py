"""Entry point for the offline Ultron prototype."""

from __future__ import annotations

import argparse

from ultron.assistant import UltronAssistant


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the offline Ultron prototype.")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="run the local assistant without network or external model access",
    )
    args = parser.parse_args()

    if not args.offline:
        parser.error("this prototype is offline-only; run with --offline")

    assistant = UltronAssistant()
    print(assistant.greeting())
    while True:
        try:
            request = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nUltron> Session ended.")
            return 0

        if not request:
            continue
        response = assistant.handle(request)
        print(f"Ultron> {response.message}")
        if response.should_exit:
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
