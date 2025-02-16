from collections import Counter
from dataclasses import dataclass
from typing import Optional, Dict, List
from queue import PriorityQueue
from tqdm import tqdm, trange
from pathlib import Path
from collections import deque
import json
import plotly.graph_objects as go
from treelib import Tree  # Add to imports at top

K = 27

# https://norvig.com/mayzner.html
# https://www.cs.umd.edu/content/punctuation-input-touchscreen-keyboards-analyzing-frequency-use-and-costs
LETTER_FREQUENCIES = {
    "e": 11.58,
    "a": 7.52,
    "o": 7.07,
    "t": 8.57,
    "i": 7.08,
    "n": 6.74,
    "s": 6.15,
    "h": 4.71,
    "l": 3.82,
    "r": 5.86,
    "m": 2.38,
    "d": 3.55,
    "u": 2.55,
    "y": 1.55,
    "g": 1.75,
    "c": 3.13,
    "k": 0.52,
    "w": 1.55,
    "b": 1.40,
    "p": 2.00,
    "f": 2.23,
    "v": 0.99,
    "j": 0.16,
    "z": 0.09,
    "x": 0.22,
    "q": 0.11,
    ">": 1.151,  # Enter
    # ",": 2.3,  # Override
    # "?": 0.032,
}


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
        dict: Contains 'codes' mapping and serialized 'tree' structure
    """
    total_freq = sum(char_freq.values())

    # Build codes and tree visualization in single BFS
    code_map = {}
    tree = Tree()
    tree.create_node("ROOT", "root", data=f"{root.freq:.1f}")

    queue = deque([(root, "", "root")])
    while queue:
        node, code, parent_id = queue.popleft()
        node.code = code
        node_id = f"{parent_id}_{code}"

        if node.char:  # Leaf node
            code_map[node.char] = code
            label = f"{code[-1:]}: {node.char}: ({node.freq/total_freq*100:.1f}%)"
            tree.create_node(label, node_id, parent=parent_id)
        else:
            tree.create_node(code[-1:], node_id, parent=parent_id)

        if node.left:
            queue.append((node.left, code + "0", node_id))
        if node.right:
            queue.append((node.right, code + "1", node_id))

    # Print tree with fixed-width formatting
    for l in tree.show(line_type="ascii-em", idhidden=True, stdout=False):
        print(l, end="")

    return {
        "codes": dict(sorted(code_map.items())),
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


def analyze_k_values(words: List[str], k_range=range(1, K + 1)):
    """Find change in average prefix length E(l) as function of k, number of codewords.
    Annotates plot with new characters added at each K.
    """
    char_freq = LETTER_FREQUENCIES  # analyze_frequencies(words)
    avg_lengths = []
    alphabet_sets = []  # Cache alphabet sets for each k

    for k in k_range:
        # Build tree and get codes for this K
        root, top_chars = build_huffman_tree(char_freq, top_k=k)
        json_output = build_prefix_code(root, char_freq)
        codes = json_output["codes"]
        alphabet_sets.append(set(codes.keys()))

        # Calculate weighted average prefix length
        total_freq = sum(char_freq.values())
        avg_length = sum(
            len(codes.get(char, "")) * freq / total_freq
            for char, freq in char_freq.items()
            if char in codes
        )
        avg_lengths.append(avg_length)

    # Create plotly figure with annotations
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(k_range),
            y=avg_lengths,
            mode="lines+markers",
            name="Average Prefix Length",
        )
    )

    # Add annotations for new characters at each k
    for i in range(len(alphabet_sets) - 1, 0, -1):
        new_chars = alphabet_sets[i] - alphabet_sets[i - 1]
        if new_chars:
            fig.add_annotation(
                x=list(k_range)[i],
                y=avg_lengths[i],
                text=f"+{','.join(sorted(list(new_chars)))}",
                showarrow=True,
                arrowhead=1,
                yshift=5,
            )

    fig.update_layout(
        title="Average Huffman Code Length vs K",
        xaxis_title="K (Alphabet Size)",
        yaxis_title="Average Code Length (bits)",
        template="plotly_white",
    )

    fig.write_image("huffman_analysis.png")


def main():
    with Path("english.txt").open() as f:
        words = [w.strip() for w in f.readlines()]

    analyze_k_values(words)  # Add analysis before original logic

    char_freq = LETTER_FREQUENCIES  # analyze_frequencies(words)
    huffman_root, top_chars = build_huffman_tree(char_freq, top_k=K)
    json_output = build_prefix_code(huffman_root, char_freq)

    with Path("english'.txt").open("w") as f:
        for w in restrict_dictionary(words, top_chars):
            f.write(w + "\n")

    with Path("huffman.json").open("w") as f:
        f.write(json.dumps(json_output, indent=2))


if __name__ == "__main__":
    main()
