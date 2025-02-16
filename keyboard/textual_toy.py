from textual.app import App
from textual.widgets import Input, Label
from textual.containers import Container
from textual.validation import ValidationResult, Validator
from pathlib import Path
import json

with Path("english'.txt").open() as f:
    WORDS = set(f.read().splitlines())
with Path("huffman.json").open() as f:
    HUFFMAN = json.load(f)["codes"]
    for k, v in HUFFMAN.items():
        assert len(k) == 1  # Single char
        assert all(c in "01" for c in v)  # has binary code
# implicit assert every char in WORDS has HUFFMAN key


class WordValidator(Validator):
    """Validates if word exists in dictionary."""

    def validate(self, value: str) -> ValidationResult:
        # keys is hashmap, O(1) lookup per c. O(n) total, n = len(value)
        if all(c in HUFFMAN.keys() for c in value):
            return ValidationResult.success()
        return ValidationResult.failure("✗")


class WordValidatorApp(App):
    """Live word validation TUI app."""

    BINDINGS = [("ctrl+c", "quit")]  # Add keyboard bindings

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def compose(self):
        """Create app layout."""
        yield Container(
            Input(
                placeholder="Type a word...",
                id="word_input",
                validators=[WordValidator()],
            ),
            Label(
                "Empty Huffman code",
                id="huffman_display",
            ),
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes and update Huffman code display."""
        if event.input.id == "word_input":
            validation = event.validation_result
            huffman_display = self.query_one("#huffman_display", Label)

            if validation.is_valid:
                huffman_display.update("".join(HUFFMAN[c] for c in event.input.value))
            else:
                huffman_display.update("")


if __name__ == "__main__":
    app = WordValidatorApp()
    app.run()
