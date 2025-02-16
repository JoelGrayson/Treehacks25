"""BCI client that reads from device and sends events via WebSocket."""

import websocket
import json
import time
import pickle
import numpy as np
from pathlib import Path
from app.services.bci import bci_session, process_board_data
from app.config.settings import settings
from app.models import StateBit, BitEvent, GreekWaves
from app.keyboard.constants import HUFFMAN
from dataclasses import asdict
from tqdm import tqdm
from typing import List, Tuple


def generate_mock_events(
    word: str = "joyful", samples_per_bit: int = 10
) -> List[BitEvent]:
    """Generate mock BitEvents for simulating typing a word.

    Args:
        word: Word to generate bits for
        samples_per_bit: Number of samples to generate per bit

    Returns:
        List of BitEvents corresponding to the Huffman encoding of the word
    """
    # Convert word to bit sequence using Huffman encoding
    bit_sequence = []
    for char in word.lower():
        bit_sequence.extend([int(b) for b in HUFFMAN[char]])

    print(f"Requested seq: {bit_sequence}")

    # Generate events
    events = []
    baseline = np.random.normal(0, 1, (20, 250))

    for bit in bit_sequence:
        # Generate samples_per_bit frames with the target bit
        for _ in range(samples_per_bit):
            frame = np.random.normal(0, 1, (20, 250))
            # Add bias to channels based on bit
            if bit == 1:
                frame[1] += 3  # Right clench
            else:
                frame[9] += 3  # Left clench

            events.append(
                BitEvent(
                    bit=StateBit.RIGHT_CLENCH if bit == 1 else StateBit.LEFT_CLENCH,
                    greeks=GreekWaves(
                        delta=np.random.random(),
                        theta=np.random.random(),
                        alpha=np.random.random(),
                        beta=np.random.random(),
                        gamma=np.random.random(),
                    ),
                    raw_data=(frame.mean(axis=1) - baseline.mean(axis=1)).tolist(),
                )
            )

        # Add neutral samples between bits
        for _ in range(samples_per_bit // 2):
            events.append(
                BitEvent(
                    bit=StateBit.NOTHING,
                    greeks=GreekWaves(
                        delta=np.random.random(),
                        theta=np.random.random(),
                        alpha=np.random.random(),
                        beta=np.random.random(),
                        gamma=np.random.random(),
                    ),
                    raw_data=(
                        np.random.normal(0, 1, 20) - baseline.mean(axis=1)
                    ).tolist(),
                )
            )

    return events


def test_mock_events():
    """Sanity tests for mock event generation."""
    # Test basic event generation
    events = generate_mock_events("j")
    assert len(events) > 0
    assert all(isinstance(e, BitEvent) for e in events)

    print(f"Had events: {events}")

    assert len(events) == len(HUFFMAN["j"])

    # Test Huffman encoding correctness
    events = generate_mock_events("j")
    bit_sequence = []
    for e in events:
        if e.bit != StateBit.NOTHING:
            bit_sequence.append("1" if e.bit == StateBit.RIGHT_CLENCH else "0")
    assert (
        "".join(bit_sequence) == HUFFMAN["j"]
    ), f"got {bit_sequence} expected {HUFFMAN['j']}"

    # Test event structure
    event = events[0]
    assert hasattr(event, "bit")
    assert hasattr(event, "greeks")
    assert hasattr(event, "raw_data")
    assert len(event.raw_data) == 8  # 8 channels
    assert all(isinstance(x, float) for x in event.raw_data)

    print("All mock event tests passed!")


# test_mock_events()


def loop_forever_bci(fetch_data, baseline, ws, delay):
    """Run BCI processing loop with configurable data source."""
    i = 0
    pbar = tqdm(unit=" bits")
    last_check = time.time()
    last_bit = StateBit.NOTHING

    while True:
        if time.time() - last_check < delay:
            continue

        event_data = process_board_data(fetch_data(i), baseline, last_bit)
        last_bit = event_data.bit
        if event_data.bit != StateBit.NOTHING:
            ws.send(json.dumps({"event": "bit", "data": asdict(event_data)}))
            pbar.update(1)
            pbar.set_postfix(bit=event_data.bit.value)
        else:
            pbar.set_postfix(bit="-1")
        i += 1
        last_check = time.time()


try:
    ws = websocket.WebSocket()
    ws.connect(f"ws://{settings.HOST}:{settings.PORT}/ws")
    if settings.SIMULATE:
        mock_events = generate_mock_events()
        i = 0
        pbar = tqdm(unit=" bits")
        last_check = time.time()

        while True:
            if time.time() - last_check < 0.1:  # Fixed 0.1s delay for simulation
                continue

            event = mock_events[i % len(mock_events)]
            if event.bit != StateBit.NOTHING:
                ws.send(json.dumps({"event": "bit", "data": asdict(event)}))
                pbar.update(1)
                pbar.set_postfix(bit=event.bit.value)
            else:
                pbar.set_postfix(bit="-1")
            i += 1
            last_check = time.time()
    else:
        with bci_session() as board:
            baseline_data = board.get_board_data()
            loop_forever_bci(
                fetch_data=lambda _: board.get_board_data(),
                baseline=baseline_data,
                ws=ws,
                delay=1,
            )
finally:
    ws.abort()
    pass
    # if ws.connected:
    #     ws.close()


if __name__ == "__main__":
    test_mock_events()
