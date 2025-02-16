from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter
from contextlib import contextmanager
import numpy as np
from enum import Enum

import time
from brainflow.board_shim import BoardShim, BoardIds
import json
import pickle
from typing import Literal
from dataclasses import dataclass

MODE: Literal['inference'] | Literal['collect'] | Literal['simulate'] = 'collect'

class BrainBit(Enum):
    BASELINE = -1 # Ignored
    LEFT_CLENCH = 0 # Binary 0
    RIGHT_CLENCH = 1 # Binary 1
    # Control bits
    NOD = 2
    SHAKE = 3

@dataclass
class GreekWaves:
    delta: float # 0.5-4 Hz
    theta: float # 4-8 Hz
    alpha: float # 8-12 Hz
    beta: float # 12-30 Hz
    gamma: float # 30-100 Hz

# https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
BOARD_ID=BoardIds.CYTON_DAISY_BOARD.value #2 #CYTON_DAISY_BOARD
PARAMS=BrainFlowInputParams()
PARAMS.serial_port='/dev/cu.usbserial-DP05IK99'

# Calibrated for Joe Li over-ear BCI, 12am
ACCEL_PITCH_THRES = 0.14
ACCEL_ROLL_THRES = 0.14
CLENCH_THRES = 200

@contextmanager
def bci_session(board_id = BOARD_ID, params = PARAMS, flush=4):
    board = BoardShim(board_id, params)
    print("Preparing")
    board.prepare_session()
    print("Connected")
    board.start_stream()
    for _ in range(flush):
        # Flush BCI signal for 3s, wait to stabilize.
        time.sleep(1)
        board.get_board_data()
    try:
        yield board
    finally:
        board.stop_stream()
        board.release_session()

def run(ws):
    start = time.time()
    # https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
    with bci_session() as board:
        bit = BrainBit.BASELINE
        i = 0
        data_to_pickle = []
        while (True):
            time.sleep(1)
            data = board.get_board_data()
            if MODE == 'collect':
                if i < 20:
                    data_to_pickle += [data]
                    i += 1
                elif i == 20:
                    with open(f"eeg_data.pkl", 'wb') as f:
                        pickle.dump(data_to_pickle, f)
                    

            eeg_channels = BoardShim.get_eeg_channels(BOARD_ID)
            accel_channels = BoardShim.get_accel_channels(BOARD_ID)

            sampling_rate=board.get_sampling_rate(BOARD_ID)
            band_powers = DataFilter.get_avg_band_powers(data, [channel for channel in eeg_channels], sampling_rate, True)[0]
            greeks = GreekWaves(
                delta=band_powers[0],
                theta=band_powers[1],
                alpha=band_powers[2],
                beta=band_powers[3],
                gamma=band_powers[4]
            )
            #print(f"Arousal: {greeks.alpha + greeks.beta}")

            # Clench movements detected by EEG
            range_left = np.ptp(data[eeg_channels[1]])
            range_right = np.ptp(data[eeg_channels[9]])

            # Head movements detected by Acceleromter (Z pitch is head nod, X roll is shake)
            range_accel_nod = np.ptp(data[accel_channels[2]])
            range_accel_shake = np.ptp(data[accel_channels[0]])

            if range_accel_nod > range_accel_shake and range_accel_nod > ACCEL_PITCH_THRES and bit.value < 2:
                bit = BrainBit.NOD
            elif range_accel_shake > range_accel_nod and range_accel_shake > ACCEL_ROLL_THRES and bit.value < 2:
                bit = BrainBit.SHAKE
            elif bit.value >= 2 or (range_left < CLENCH_THRES and range_right < CLENCH_THRES):
                bit = BrainBit.BASELINE
            elif range_left > range_right:
                bit = BrainBit.LEFT_CLENCH
            elif range_right > range_left:
                bit = BrainBit.RIGHT_CLENCH

            ws.send(json.dumps({"type": "bit", "data": bit.value}))
            print(f"{(time.time() - start):.2f}s: {bit.value} ({bit.name})")