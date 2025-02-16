from typing import List, Optional, Tuple
from app.models import WordEvent, WordSuggestion, StateBit
from app.keyboard.textual_toy import AutocorrectEngine


async def handle(
    bit: StateBit,
    current_bits: str,
    autocorrect: AutocorrectEngine,
) -> Tuple[str, Optional[WordEvent]]:
    """Process a bit and return updated state and optional word event"""
    if bit in (StateBit.LEFT_CLENCH, StateBit.RIGHT_CLENCH):
        new_bits = current_bits + str(bit.value)
        suggestions = await autocorrect.get_suggestions(new_bits)

        print(suggestions)

        if len(suggestions) == 1:
            return new_bits, WordEvent(
                bits=new_bits,
                suggestions=[],
                complete_word=suggestions[0],
            )

        return new_bits, WordEvent(
            bits=new_bits,
            suggestions=suggestions,
            complete_word=None,
        )

    elif bit == StateBit.NOD:
        # Accept current word, reset state
        return "", None

    elif bit == StateBit.SHAKE:
        # Backspace
        return current_bits[:-1] if current_bits else "", None

    return current_bits, None
