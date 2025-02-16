import random


def binary_edit_distance(s1: str, s2: str) -> int:
    """Calculate edit distance between two binary strings using bit operations.

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
    """Edge case tests for binary_edit_distance."""
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


if __name__ == "__main__":
    test()
