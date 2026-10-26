import tempfile
import unittest
from pathlib import Path

from ultron.assistant import UltronAssistant
from ultron.memory import MemoryStore


class AssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.assistant = UltronAssistant(
            MemoryStore(Path(self.temp_dir.name) / "memory.json")
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_remember_and_recall(self) -> None:
        self.assertIn("Saved", self.assistant.handle("/remember build a sensor").message)
        self.assertIn("build a sensor", self.assistant.handle("/recall").message)

    def test_calculator_rejects_code(self) -> None:
        self.assertIn("only arithmetic", self.assistant.handle("/calc __import__('os')").message)
        self.assertEqual("2 + 3 = 5", self.assistant.handle("/calc 2 + 3").message)

    def test_quit(self) -> None:
        response = self.assistant.handle("/quit")
        self.assertTrue(response.should_exit)

    def test_natural_language_shortcuts(self) -> None:
        self.assertIn("Local time:", self.assistant.handle("what time is it").message)
        self.assertIn("Offline and ready", self.assistant.handle("show status").message)


if __name__ == "__main__":
    unittest.main()
