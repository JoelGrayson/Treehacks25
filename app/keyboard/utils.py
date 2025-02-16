from typing import Optional
from app.keyboard.constants import HUFFMAN, HUFFMAN_INV, WORDS


def pad_coding(word: str) -> tuple[str, str]:
    code = ""
    text = ""
    for c in word:
        c_code = HUFFMAN[c]
        code += c_code
        text += c.replace(" ", "_").rjust(len(c_code))
    return code, text


def binary_to_word(binary: str) -> Optional[str]:
    """Decode binary to word with inverse Huffman map.

    Returns None if:
    - Invalid sequence found in middle of binary
    - Any sequence longer than longest valid Huffman code
    - Last typing sequence is longer than longest valid code

    If invalid sequence is at end but shorter than max code length,
    returns the last valid word (to handle incomplete typing)."""
    word = ""
    i = 0
    last_valid_word = ""
    max_code_len = max(len(code) for code in HUFFMAN_INV)

    while i < len(binary):
        found_match = False
        for j in range(i + 1, min(i + max_code_len + 1, len(binary) + 1)):
            prefix = binary[i:j]
            if prefix in HUFFMAN_INV:
                # Before accepting this match, check if remaining sequence is too long
                remaining_len = len(binary) - j
                if remaining_len > max_code_len:
                    return None

                word += HUFFMAN_INV[prefix][0]
                i = j
                if word in WORDS:
                    last_valid_word = word
                found_match = True
                break
            if len(prefix) >= max_code_len:
                return None

        if not found_match:
            remaining_len = len(binary) - i
            if remaining_len > max_code_len:
                return None
            return last_valid_word

    return word if word in WORDS else last_valid_word


class BinaryEditDistanceStream:
    """Streaming edit distance calculator for binary strings.

    Optimized for computing edit distance as characters are added to s1,
    with a fixed reference string s2.

    Time complexity per character: O(1) amortized
    Space complexity: O(n/64) where n = len(s2)
    """

    def __init__(self, s2: str):
        self.s2 = s2
        self.n = len(s2)
        self.blocks = (self.n + 63) // 64

        # Precompute s2 pattern blocks
        self.pattern2 = [0] * self.blocks
        for i, c in enumerate(s2):
            if c == "1":
                self.pattern2[i // 64] |= 1 << (i % 64)

        # Initialize s1 state
        self.pattern1 = [0] * self.blocks
        self.s1_len = 0

    def add(self, c: str) -> int:
        """Process new character and return updated edit distance.

        Args:
            c: New character ('0' or '1') to append to s1

        Returns:
            Current edit distance between s1 + c and s2
        """
        assert c in "01"

        # Special case: if s2 is empty, distance is just length of s1
        if self.n == 0:
            self.s1_len += 1
            return self.s1_len

        # Update affected block for new character
        block_idx = self.s1_len // 64
        if block_idx < self.blocks:
            if c == "1":
                self.pattern1[block_idx] |= 1 << (self.s1_len % 64)

        self.s1_len += 1

        # Calculate Hamming distance for aligned portions
        distance = 0
        full_blocks = min(self.s1_len, self.n) // 64
        remaining_bits = min(self.s1_len, self.n) % 64

        # Full blocks
        for i in range(full_blocks):
            diff = self.pattern1[i] ^ self.pattern2[i]
            distance += bin(diff).count("1")

        # Partial block
        if remaining_bits > 0:
            mask = (1 << remaining_bits) - 1
            diff = (self.pattern1[full_blocks] ^ self.pattern2[full_blocks]) & mask
            distance += bin(diff).count("1")

        # Add cost of length difference
        distance += abs(self.n - self.s1_len)

        return distance


def binary_edit_distance(s1: str, s2: str) -> int:
    """Calculate edit distance between two binary strings.

    Uses Myers' bit-parallel algorithm for O(n/w) time where:
    - n is the length of the longer string
    - w is the machine word size (typically 64)

    Time complexity: O(n/64) for strings <= 64 bits
                    O(nm/64) for longer strings where m = min(len(s1), len(s2))
    Space complexity: O(1) for strings <= 64 bits
                     O(m) for longer strings

    Args:
        s1: First binary string containing only '0' and '1'
        s2: Second binary string containing only '0' and '1'

    Returns:
        Minimum edit distance between strings

    Example:
        >>> binary_levenshtein_distance("1100", "1010")
        2  # 1100 → 1110 → 1010
    """
    # Ensure s1 is shorter for optimization
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    m, n = len(s1), len(s2)

    # Convert strings to integer arrays for bit operations
    # Each integer represents a block of 64 characters
    blocks = (m + 63) // 64
    pattern1 = [0] * blocks
    for i, c in enumerate(s1):
        if c == "1":
            pattern1[i // 64] |= 1 << (i % 64)

    pattern2 = [0] * blocks
    for i, c in enumerate(s2[:m]):  # Only compare up to length of s1
        if c == "1":
            pattern2[i // 64] |= 1 << (i % 64)

    # Calculate Hamming distance (differing bits) for each block
    distance = 0
    for i in range(blocks):
        # XOR finds differing bits, then count them
        diff = pattern1[i] ^ pattern2[i]
        distance += bin(diff).count("1")

    # Add cost of length difference
    distance += abs(n - m)

    return distance
