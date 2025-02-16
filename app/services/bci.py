from contextlib import contextmanager
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter
import numpy as np

import time
from app.models import GreekWaves, StateBit, BitEvent
from app.config.settings import settings


def get_greek_waves(data: np.ndarray, sampling_rate: int) -> GreekWaves:
    """Extract frequency band powers from EEG data"""
    eeg_channels = BoardShim.get_eeg_channels(settings.board_id)

    band_powers = DataFilter.get_avg_band_powers(
        data, eeg_channels, sampling_rate, True
    )[0]

    return GreekWaves(
        delta=band_powers[0],
        theta=band_powers[1],
        alpha=band_powers[2],
        beta=band_powers[3],
        gamma=band_powers[4],
    )


def action_to_state(
    range_left: float,
    range_right: float,
    range_accel_nod: float,
    range_accel_shake: float,
    last_bit: StateBit,
) -> StateBit:
    """Detect movement type based on sensor ranges"""
    if last_bit == StateBit.NOTHING:
        if (
            range_accel_nod > range_accel_shake
            and range_accel_nod > settings.accel_pitch_thres
        ):
            return StateBit.NOD
        elif (
            range_accel_shake > range_accel_nod
            and range_accel_shake > settings.accel_roll_thres
        ):
            return StateBit.SHAKE
        elif range_left > range_right and range_left > settings.left_clench_thres:
            return StateBit.LEFT_CLENCH
        elif range_right > range_left and range_right > settings.right_clench_thres:
            return StateBit.RIGHT_CLENCH
    return StateBit.NOTHING


def process_board_data(
    data: np.ndarray,
    baseline_data: np.ndarray,
    last_bit: StateBit,
) -> BitEvent:
    """Process raw board data into bit event"""
    eeg_channels = BoardShim.get_eeg_channels(settings.board_id)
    accel_channels = BoardShim.get_accel_channels(settings.board_id)
    sampling_rate = BoardShim.get_sampling_rate(settings.board_id)

    range_left = np.ptp(data[eeg_channels[1]])
    range_right = np.ptp(data[eeg_channels[9]])
    range_accel_nod = np.ptp(data[accel_channels[2]])
    range_accel_shake = np.ptp(data[accel_channels[0]])

    if not settings.SIMULATE:
        print(range_left, range_right, range_accel_nod, range_accel_shake)

    bit = action_to_state(
        range_left,
        range_right,
        range_accel_nod,
        range_accel_shake,
        last_bit,
    )

    return BitEvent(
        bit=bit,
        greeks=get_greek_waves(data, sampling_rate),
        raw_data=(np.mean(data, axis=1) - np.mean(baseline_data, axis=1)).tolist(),
    )


@contextmanager
def bci_session(flush_seconds: int = 4):
    """Context manager for BCI board session"""
    board_params = BrainFlowInputParams()
    board_params.serial_port = settings.serial_port

    board = BoardShim(settings.board_id, board_params)
    print("Preparing BCI connection...")
    board.prepare_session()
    board.start_stream()

    # Flush initial noisy data
    for _ in range(flush_seconds):
        time.sleep(1)
        board.get_board_data()

    try:
        yield board
    finally:
        board.stop_stream()
        board.release_session()
