"""EEG data exploration script for analyzing pickled EEG recordings."""

import pickle
from pathlib import Path
from brainflow.board_shim import BoardShim, BoardIds

BOARD_ID = BoardIds.CYTON_DAISY_BOARD.value  # 2 #CYTON_DAISY_BOARD
eeg_c = BoardShim.get_eeg_channels(BOARD_ID)
acc_c = BoardShim.get_accel_channels(BOARD_ID)

with Path("eeg_data.pkl").open("rb") as f:
    data = pickle.load(f)

for i, c in enumerate(eeg_c):
    print(f"eeg {i} (idx={c}): {data[0][c][:5]} ...")

for i, c in enumerate(acc_c):
    print(f"acc {i} (idx={c}): {data[0][c][:5]} ...")

print(len(data[0][c]))
