from textual.app import App
from textual.widgets import Input, Label
from textual.containers import Container
from textual.validation import ValidationResult, Validator
from queue import PriorityQueue
from utils import (
    binary_edit_distance,
    pad_coding,
    binary_to_word,
    BinaryEditDistanceStream,
)
from constants import HUFFMAN, FREQ_WORDS
from dataclasses import dataclass, field
import asyncio


@dataclass
class AutocorrectEngine:
    """Maintains streaming edit distance state for word suggestions."""

    word_streams: dict[str, BinaryEditDistanceStream] = field(default_factory=dict)

    def __post_init__(self):
        for word in FREQ_WORDS:
            code = "".join(HUFFMAN[c] for c in word)
            self.word_streams[word] = BinaryEditDistanceStream(code)

    async def get_suggestions(self, binary: str, threshold: int = 2) -> list[str]:
        """Get suggestions with chunked processing."""
        results = []
        pq = PriorityQueue()

        direct = binary_to_word(binary)
        if direct is not None:
            return [direct]

        # Process words in chunks to stay responsive
        CHUNK_SIZE = 100
        for i in range(0, len(FREQ_WORDS), CHUNK_SIZE):
            chunk = FREQ_WORDS[i : i + CHUNK_SIZE]
            for word in chunk:
                stream = self.word_streams[word]
                dist = stream.add(binary[-1]) if binary else 0

                if dist < threshold:
                    results.append((dist, word))
                    if len(results) >= 5:
                        return [word for _, word in sorted(results)]
                else:
                    pq.put((dist, word))

            await asyncio.sleep(0)

        while len(results) < 5 and not pq.empty():
            results.append(pq.get())

        return [word for _, word in sorted(results)]

    def reset(self) -> None:
        for word in FREQ_WORDS:
            code = "".join(HUFFMAN[c] for c in word)
            self.word_streams[word] = BinaryEditDistanceStream(code)


class WordValidator(Validator):
    """Validates if word exists in dictionary."""

    def validate(self, value: str) -> ValidationResult:
        # keys is hashmap, O(1) lookup per c. O(n) total, n = len(value)
        if all(c in HUFFMAN.keys() for c in value):
            return ValidationResult.success()
        return ValidationResult.failure("✗")


class BinaryValidator(Validator):
    """Validates if input is binary string."""

    def validate(self, value: str) -> ValidationResult:
        if all(c in "01" for c in value):
            return ValidationResult.success()
        return ValidationResult.failure("✗")


class WordValidatorApp(App):
    """TUI app for bidirectional word/binary conversion with suggestions."""

    autocorrect: AutocorrectEngine

    def compose(self):
        self.autocorrect = AutocorrectEngine()
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
            Input(
                placeholder="Type binary...",
                id="binary_input",
                validators=[BinaryValidator()],
            ),
            Label(
                "Empty word",
                id="word_display",
            ),
        )

    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes and update displays."""
        if event.input.id == "word_input":
            validation = event.validation_result
            huffman_display = self.query_one("#huffman_display", Label)

            if validation.is_valid:
                code, letters = pad_coding(event.input.value)
                huffman_display.update(f"{code}\n{letters}")
            else:
                huffman_display.update("")

        elif event.input.id == "binary_input" and event.validation_result.is_valid:
            word_display = self.query_one("#word_display", Label)

            if not event.input.value:
                self.autocorrect.reset()
                word_display.update("")
                return

            suggestions = await self.autocorrect.get_suggestions(event.input.value)
            word_display.update("\n".join(suggestions))


if __name__ == "__main__":
    app = WordValidatorApp()
    app.run()
