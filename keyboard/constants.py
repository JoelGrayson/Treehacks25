from pathlib import Path
import json

with Path("english'.txt").open() as f:
    WORDS = set(f.read().splitlines())
with Path("huffman.json").open() as f:
    HUFFMAN = json.load(f)["codes"]
    for k, v in HUFFMAN.items():
        assert len(k) == 1  # Single char
        assert all(c in "01" for c in v)  # has binary code
    HUFFMAN_INV = {char: code for code, char in HUFFMAN.items()}  # Inverse map
# implicit assert every char in WORDS has HUFFMAN key

# Load frequency table
with Path("freq.txt").open() as f:
    FREQ_WORDS = f.read().splitlines()  # f ranked by line number.
