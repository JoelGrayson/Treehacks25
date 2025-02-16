import random
from typing import Iterator
from constants import HUFFMAN, HUFFMAN_INV, WORDS
from utils import binary_edit_distance, BinaryEditDistanceStream, binary_to_word


# Random bit flip tests
def _flip_bits(s: str, n: int) -> str:
    """Flip n random bits in binary string s."""
    assert all(c in ["0", "1"] for c in s)
    positions = random.sample(range(len(s)), n)
    s_list = list(s)
    for pos in positions:
        s_list[pos] = "1" if s_list[pos] == "0" else "0"
    return "".join(s_list)


def test():
    """Edge case tests for binary_edit_distance and BinaryEditDistanceStream."""
    import random

    random.seed(42)  # Deterministic testing

    # Original edge cases
    assert binary_edit_distance(s1="", s2="") == 0
    assert binary_edit_distance(s1="", s2="1") == 1
    assert binary_edit_distance(s1="1", s2="") == 1
    assert binary_edit_distance(s1="0", s2="1") == 1
    assert binary_edit_distance(s1="1", s2="1") == 0
    assert binary_edit_distance(s1="1" * 64, s2="0" * 64) == 64
    assert binary_edit_distance(s1="1" * 63, s2="0" * 63) == 63
    assert binary_edit_distance(s1="1" * 65, s2="0" * 65) == 65
    assert binary_edit_distance(s1="10" * 32, s2="01" * 32) == 64
    assert binary_edit_distance(s1="1" * 1000, s2="1" * 100) == 900

    # Test with different string lengths and flip counts
    test_cases = [
        (63, 10),  # Just under word size
        (64, 20),  # Exact word size
        (65, 30),  # Just over word size
        (128, 40),  # Two words
        (1000, 100),  # Many words
    ]

    for length, flips in test_cases:
        s1 = "1" * length
        s2 = _flip_bits(s1, flips)
        assert binary_edit_distance(s1=s1, s2=s2) == flips

    print("All pass")


def _stream_vs_batch(s1: str, s2: str):
    """Compare streaming vs batch results"""
    calculator = BinaryEditDistanceStream(s2)
    streaming_results = []
    for c in s1:
        streaming_results.append(calculator.add(c))
    batch_results = [binary_edit_distance(s1[: i + 1], s2) for i in range(len(s1))]
    assert streaming_results == batch_results, (
        f"Mismatch for s1={s1}, s2={s2}:\n"
        f"Streaming: {streaming_results}\n"
        f"Batch:     {batch_results}"
    )


def test_stream():
    # Diabolical test cases
    test_cases = [
        # Empty and single char cases
        "",
        "1",
        # Block boundary cases
        "1" * 63,
        "1" * 64,
        "1" * 65,
        # Mixed patterns at block boundaries
        "1" * 63 + "0",
        "1" * 64 + "0",
        "0" + "1" * 63,
        # Alternating patterns
        "10" * 32,
        "01" * 32,
        "10" * 33,
        # Random flips near block boundaries
        _flip_bits("1" * 64, 10),
        _flip_bits("0" * 64 + "1" * 64, 20),
        # Long strings with sparse differences
        "1" * 1000 + "0" + "1" * 1000,
        _flip_bits("1" * 2048, 100),
    ]

    # Test all pairs
    for s1 in test_cases:
        for s2 in test_cases:
            _stream_vs_batch(s1, s2)

    # Specific evil cases
    evil_pairs = [
        # Each pair is [s1, s2]
        ["1", "1" * 1000],
        ["1" * 1000, "1"],
        # Block alignment stress tests
        ["1" * 63 + "0" * 65, "0" * 63 + "1" * 65],
        ["1" * 64 + "0" * 64, "0" * 64 + "1" * 64],
        # Alternating patterns with offsets
        ["10" * 32, "01" * 32],
        ["10" * 32 + "1", "01" * 32 + "0"],
        # Random but reproducible chaos
        [_flip_bits("1" * 127, 63), _flip_bits("0" * 127, 63)],
        [_flip_bits("10" * 64, 64), _flip_bits("01" * 64, 64)],
    ]

    for s1, s2 in evil_pairs:
        _stream_vs_batch(s1, s2)
        # Test with swapped inputs
        _stream_vs_batch(s2, s1)

    # Stress test with random streams
    for _ in range(100):
        length = random.randint(1, 2048)
        s1 = "".join(random.choice("01") for _ in range(length))
        s2 = "".join(random.choice("01") for _ in range(length))
        _stream_vs_batch(s1, s2)

    print("All pass: stream")


def invalid_seq_candidates(max_code_len: int) -> Iterator[str]:
    """Generate candidate invalid sequences.

    By Kraft's inequality, for any length L > max_code_len, there must exist
    sequences of length L that are not prefixes of any valid code.

    Yields candidates in order of increasing complexity:
    1. Simple repeating patterns
    2. Systematic enumeration"""
    L = max_code_len + 1

    # Simple patterns first
    yield "0" * L
    yield "1" * L

    # Then systematic enumeration
    for i in range(2**L):
        candidate = format(i, f"0{L}b")
        yield candidate


def make_invalid_seq(max_code_len: int) -> str:
    """Find a binary string that cannot be the encoding of any sequence of symbols.

    Strategy:
    1. Find a proper prefix of some codeword that isn't itself a complete codeword
    2. If no such prefix exists, try exhaustive search of short binary strings

    Args:
        max_code_len: Maximum length of any Huffman code

    Returns:
        A binary string that cannot be decoded using the Huffman coding
    """
    codewords = set(HUFFMAN.values())

    # Try to find a proper prefix of a codeword that isn't itself a codeword
    for cw in codewords:
        for i in range(1, len(cw)):
            prefix = cw[:i]
            if prefix not in codewords:
                # Repeat prefix to exceed max_code_len to ensure it's invalid
                repeats = (max_code_len + 1) // len(prefix) + 1
                return (prefix * repeats)[: max_code_len + 1]

    # If no proper prefix found, try exhaustive search of short strings
    def is_valid_encoding(s: str) -> bool:
        """Check if string can be segmented into valid codewords."""
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(n):
            if dp[i]:
                for cw in codewords:
                    if s.startswith(cw, i):
                        dp[i + len(cw)] = True
        return dp[n]

    # Try binary strings of increasing length
    for length in range(1, max_code_len + 2):
        for i in range(2**length):
            candidate = format(i, f"0{length}b")
            if not is_valid_encoding(candidate):
                # Found invalid sequence, repeat to exceed max_code_len
                repeats = (max_code_len + 1) // len(candidate) + 1
                return (candidate * repeats)[: max_code_len + 1]

    raise ValueError("Could not find invalid sequence - code appears to be complete")


def test_binary_to_word():
    """Stress test binary_to_word with evil edge cases."""
    import random

    random.seed(42)

    invalid_seq = make_invalid_seq(max(len(code) for code in HUFFMAN_INV))

    print(f"Incorrect sequence: {invalid_seq}")

    # Get list of valid codes for random sampling
    valid_codes = list(HUFFMAN_INV.keys())

    # Generate evil test cases
    test_cases = []

    # Basic invalid cases - only completely invalid sequences from start should be None
    test_cases.extend(
        [
            ("", None),
            ("0", None),  # Invalid from start
        ]
    )

    # Valid prefixes with invalid endings - should return last valid word
    for _ in range(20):
        n = random.randint(1, 5)
        valid_seq = ""
        valid_word = ""
        last_valid = None
        approx_cases = []
        for _ in range(n):
            code = random.choice(valid_codes)
            valid_seq += code
            valid_word += HUFFMAN_INV[code][0]
            if valid_word in WORDS:
                last_valid = valid_word
                # Add case: valid word + invalid ending
                approx_cases.append(valid_seq + invalid_seq)
                # Add case: valid word + partial valid code
                next_code = random.choice(valid_codes)
                approx_cases.append(valid_seq + next_code[:-1])
        for c in approx_cases:
            result = binary_to_word(c)
            assert (
                result is not None
            ), f"Failed for {c!r}: expected {last_valid!r}, got {result!r}"

    # Inject invalid sequences into middle of valid codes
    for _ in range(20):
        prefix = random.choice(valid_codes)
        suffix = random.choice(valid_codes)
        # Only None if corruption is not at end
        if HUFFMAN_INV[prefix][0] in WORDS:
            expected = HUFFMAN_INV[prefix][0]
        else:
            expected = None
        test_cases.extend(
            [
                (prefix + invalid_seq + suffix, None),  # Invalid in middle
                (prefix + "0" + suffix, None),  # Invalid in middle
                (prefix + "1" + suffix, None),  # Invalid in middle
                (prefix + invalid_seq, expected),  # Invalid at end
            ]
        )

    # Evil concatenations - None only if corruption is in middle
    for _ in range(20):
        n = random.randint(2, 4)
        codes = [random.choice(valid_codes) for _ in range(n)]
        seq = "".join(codes)
        # Insert invalid sequence at random position
        pos = random.randint(1, len(seq) - 1)
        corrupted = seq[:pos] + invalid_seq + seq[pos:]

        # Build word up to corruption point to find expected result
        word = ""
        for code in codes:
            if len(word) * 2 >= pos:  # Approximate position check
                break
            word += HUFFMAN_INV[code][0]
        expected = None if pos < len(seq) - 4 else (word if word in WORDS else None)
        test_cases.append((corrupted, expected))

    # Run all tests
    for binary, expected in test_cases:
        result = binary_to_word(binary)
        assert (
            result == expected
        ), f"Failed for {binary!r}: expected {expected!r}, got {result!r}"

    print(f"All {len(test_cases)} binary_to_word tests passed")


def test_hardcoded_regressions():
    # max_code_len = #max(len(code) for code in HUFFMAN_INV)

    assert binary_to_word("11111") == "h"
    assert binary_to_word("111") == ""

    # Should fail if last typing word is longer than longest code
    assert binary_to_word("111110" + "1" * 20) is None


if __name__ == "__main__":
    # test()
    # test_stream()
    test_hardcoded_regressions()
    # test_binary_to_word()
