from collections import Counter
from dataclasses import dataclass
from typing import Optional, Dict, List
from queue import PriorityQueue
from tqdm import tqdm
from pathlib import Path
from collections import deque
import json
import plotly.graph_objects as go

K = 26


@dataclass
class HuffmanNode:
    char: Optional[str]
    freq: int
    code: Optional[str] = None
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    def __lt__(self, other):
        return self.freq < other.freq

    def node_to_dict(self) -> dict:
        """Serialize tree of HuffmanNodes.
        Trunk nodes: only code and children
        Leaf nodes: only char, freq, and code
        """
        if self.left or self.right:
            # Trunk
            return {
                "code": self.code,
                "left": self.left.node_to_dict(),
                "right": self.right.node_to_dict(),
            }
        else:
            # Leaf
            return {
                "char": self.char,
                "freq": self.freq,
                "code": self.code,
            }


def analyze_frequencies(words: List[str]) -> Dict[str, int]:
    """Count character frequencies across all words."""
    char_freq = Counter()
    for word in tqdm(words, desc="Count freq"):
        char_freq.update(c for c in word if c.isalpha())

    total_chars = sum(char_freq.values())
    print(f"\nTotal characters analyzed: {total_chars:,}")
    return char_freq


def build_huffman_tree(
    char_freq: Dict[str, int], top_k: int
) -> tuple[HuffmanNode, List[tuple[str, int]]]:
    """Build Huffman tree from top K most frequent characters."""
    pq = PriorityQueue()

    # Get top K characters
    top_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)[:top_k]

    # Let 'space' have shortest Huffman code
    pq.put(HuffmanNode(" ", top_chars[0][1] + 1))
    for char, freq in top_chars:
        pq.put(HuffmanNode(char, freq))

    # Build tree
    while pq.qsize() > 1:
        left = pq.get()
        right = pq.get()
        internal = HuffmanNode(
            char="", freq=left.freq + right.freq, left=left, right=right
        )
        pq.put(internal)

    return pq.get(), top_chars


def build_prefix_code(
    root: HuffmanNode, char_freq: Dict[str, int]
) -> tuple[HuffmanNode, str]:
    """Assign Huffman codes and serialize tree in a single BFS traversal.

    Returns:
        tuple[HuffmanNode, str]: Root node and JSON string containing tree and codes
    """
    print("\nHuffman Codes (sorted by frequency):")
    total_freq = sum(char_freq.values())

    # Build codes and code map in single BFS
    code_map = {}
    queue = deque([(root, "")])
    while queue:
        node, code = queue.popleft()
        node.code = code

        if node.char:  # Leaf node
            code_map[node.char] = code
            percentage = (node.freq / total_freq) * 100
            print(f"{node.char}: {code} ({percentage:.2f}%)")

        if node.left:
            queue.append((node.left, code + "0"))
        if node.right:
            queue.append((node.right, code + "1"))

    return {
        "codes": dict(sorted(code_map.items())),  # Alphabetical order
        "tree": root.node_to_dict(),
    }


def restrict_dictionary(words: List[str], top_chars: List[tuple[str, int]]):
    """Compute restricted subset of dictionary where all letters are in Huffman tree."""
    charset = set(c for c, _ in top_chars)

    count = 0
    for word in tqdm(words, desc="Restrict dict"):
        if all(c in charset for c in word):
            count += 1
            yield word

    print(
        f"Saved {count:,}/{len(words):,} ~ {count/len(words)*100:.2f}% words in restricted English coding"
    )


def analyze_k_values(words: List[str], k_range: range = range(3, 27)):
    """Find change in average prefix length E(l) as function of k, number of codewords.
    Save Plotly line plot
    """
    char_freq = analyze_frequencies(words)
    avg_lengths = []

    for k in tqdm(k_range, desc="Analyzing K values"):
        # Build tree and get codes for this K
        huffman_root, _ = build_huffman_tree(char_freq, top_k=k)
        json_output = build_prefix_code(huffman_root, char_freq)
        codes = json_output["codes"]

        # Calculate weighted average prefix length
        total_freq = sum(char_freq.values())
        avg_length = sum(
            len(codes.get(char, "")) * freq / total_freq
            for char, freq in char_freq.items()
            if char in codes
        )
        avg_lengths.append(avg_length)

    # Create plotly figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(k_range),
            y=avg_lengths,
            mode="lines+markers",
            name="Average Prefix Length",
        )
    )

    fig.update_layout(
        title="Average Huffman Code Length vs K",
        xaxis_title="K (Number of Characters)",
        yaxis_title="Average Code Length (bits)",
        template="plotly_white",
    )

    fig.write_image("huffman_analysis.png")


def main():
    with Path("english.txt").open() as f:
        words = [w.strip() for w in f.readlines()]

    analyze_k_values(words)  # Add analysis before original logic

    char_freq = analyze_frequencies(words)
    huffman_root, top_chars = build_huffman_tree(char_freq, top_k=K)
    json_output = build_prefix_code(huffman_root, char_freq)

    with Path("english'.txt").open("w") as f:
        for w in restrict_dictionary(words, top_chars):
            f.write(w + "\n")

    with Path("huffman.json").open("w") as f:
        f.write(json.dumps(json_output, indent=2))


if __name__ == "__main__":
    main()
