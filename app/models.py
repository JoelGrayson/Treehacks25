from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class GreekWaves:
    delta: float  # 0.5-4 Hz
    theta: float  # 4-8 Hz
    alpha: float  # 8-12 Hz
    beta: float  # 12-30 Hz
    gamma: float  # 30-100 Hz


class StateBit(str, Enum):
    NOTHING = -1  # Ignored
    LEFT_CLENCH = 0  # Binary 0
    RIGHT_CLENCH = 1  # Binary 1
    # Control bits
    NOD = 2
    SHAKE = 3

    def __str__(self) -> int:
        return self.value


@dataclass
class BitEvent:
    """Raw bit detection from BCI device"""

    bit: StateBit
    greeks: GreekWaves
    raw_data: List[float]


@dataclass
class WordSuggestion:
    """Word suggestion with confidence score"""

    word: str
    edit_distance: float


@dataclass
class WordEvent:
    """Word detection event"""

    bits: str
    suggestions: List[str]
    complete_word: Optional[str]
