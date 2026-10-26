"""Command routing and responses for the offline Ultron prototype."""

from __future__ import annotations

import ast
import datetime as dt
import platform
import operator
from dataclasses import dataclass
from typing import Callable

from .memory import MemoryStore


@dataclass(frozen=True)
class AssistantResponse:
    message: str
    should_exit: bool = False


class UltronAssistant:
    """A deterministic assistant with safe, local capabilities."""

    def __init__(self, memory: MemoryStore | None = None) -> None:
        self.memory = memory or MemoryStore()
        self._commands: dict[str, Callable[[str], AssistantResponse]] = {
            "/help": self._help,
            "/status": self._status,
            "/time": self._time,
            "/remember": self._remember,
            "/recall": self._recall,
            "/calc": self._calculate,
            "/quit": self._quit,
            "/exit": self._quit,
        }

    def greeting(self) -> str:
        return "Online. Offline mode active. Type /help for commands."

    def handle(self, request: str) -> AssistantResponse:
        text = request.strip()
        command = text.split(maxsplit=1)[0].lower() if text else ""
        if command in self._commands:
            argument = text[len(command) :].strip()
            return self._commands[command](argument)

        lowered = text.lower()
        if "time" in lowered:
            return self._time("")
        if lowered in {"status", "show status", "system status"}:
            return self._status("")
        if lowered.startswith("remember that "):
            return self._remember(text[14:])
        if lowered in {"hello", "hi", "hey"}:
            return AssistantResponse("Hello. Systems nominal.")
        return AssistantResponse(
            "I did not recognize that request. Use /help to see safe local commands."
        )

    def _help(self, _: str) -> AssistantResponse:
        return AssistantResponse(
            "Commands: /status, /time, /remember <note>, /recall, "
            "/calc <expression>, /quit. No shell commands are executed."
        )

    def _status(self, _: str) -> AssistantResponse:
        return AssistantResponse(
            f"Offline and ready. Host: {platform.node() or 'unknown'}; "
            f"OS: {platform.system()} {platform.release()}; "
            f"Python: {platform.python_version()}."
        )

    def _time(self, _: str) -> AssistantResponse:
        now = dt.datetime.now().astimezone()
        return AssistantResponse(now.strftime("Local time: %Y-%m-%d %H:%M:%S %Z"))

    def _remember(self, note: str) -> AssistantResponse:
        if not note:
            return AssistantResponse("Usage: /remember <note>")
        self.memory.add(note)
        return AssistantResponse("Saved to local memory.")

    def _recall(self, _: str) -> AssistantResponse:
        notes = self.memory.load()
        if not notes:
            return AssistantResponse("Local memory is empty.")
        return AssistantResponse("\n".join(f"{index}. {note}" for index, note in enumerate(notes, 1)))

    def _calculate(self, expression: str) -> AssistantResponse:
        if not expression:
            return AssistantResponse("Usage: /calc <numbers and + - * / // % ** ( )>")
        try:
            result = _safe_calculate(expression)
        except (SyntaxError, ValueError, ZeroDivisionError) as exc:
            return AssistantResponse(f"Cannot calculate that safely: {exc}")
        return AssistantResponse(f"{expression} = {result}")

    def _quit(self, _: str) -> AssistantResponse:
        return AssistantResponse("Session ended.", should_exit=True)


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_calculate(expression: str) -> int | float:
    """Evaluate arithmetic syntax only; names, calls, and attributes are rejected."""
    tree = ast.parse(expression, mode="eval")

    def evaluate(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("exponent is too large")
            return _OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("only arithmetic expressions are allowed")

    return evaluate(tree)
