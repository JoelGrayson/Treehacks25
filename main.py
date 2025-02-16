from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import time
import numpy as np


from brainflow.board_shim import BoardShim, BoardIds


# https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
board_id=BoardIds.CYTON_DAISY_BOARD.value #2 #CYTON_DAISY_BOARD
params=BrainFlowInputParams()
params.serial_port='/dev/cu.usbserial-DP05IK99'


def run(ws):
    # https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
    board_id = BoardIds.CYTON_DAISY_BOARD.value  # 2 #CYTON_DAISY_BOARD
    params = BrainFlowInputParams()
    params.serial_port = "/dev/cu.usbserial-DP05IK99"

    board = BoardShim(board_id, params)
    print("PRE")
    board.prepare_session()
    print("Successfully connected")
    board.start_stream()

    eeg_channels = BoardShim.get_eeg_channels(board_id)
    accel_channels = BoardShim.get_accel_channels(board_id)
    sampling_rate = board.get_sampling_rate(board_id)

    for i in range(3):
        time.sleep(1)
        data = board.get_board_data()
    time.sleep(1)
    baseline = board.get_board_data()
    pre = -1
    while (True):
        time.sleep(1)
        data = board.get_board_data()
        eeg_channels = BoardShim.get_eeg_channels(board_id)
        accel_channels = BoardShim.get_accel_channels(board_id)
        sampling_rate=board.get_sampling_rate(board_id)

        band_powers = DataFilter.get_avg_band_powers(data, [channel for channel in eeg_channels], sampling_rate, True)
        delta, theta, alpha, beta, gamma = band_powers[0][0], band_powers[0][1], band_powers[0][2], band_powers[0][3], band_powers[0][4]
        arousal = beta + gamma
        print("Arousal:", arousal)

        # Clench movements detected by EEG
        arr_left = data[eeg_channels[1]]
        range_left = np.ptp(arr_left)

        arr_right = data[eeg_channels[9]]
        range_right = np.ptp(arr_right)

        # Head movements detected by ACC
        arr_accel_nod = data[accel_channels[2]] # Z-Axis
        range_accel_nod = np.ptp(arr_accel_nod)

        arr_accel_shake = data[accel_channels[0]] # X-axis
        range_accel_shake = np.ptp(arr_accel_shake)

        # calibration
        accel_nod_threshold = 0.14
        accel_shake_threshold = 0.14
        clench_threshold = 200

        if range_accel_nod > range_accel_shake and range_accel_nod > accel_nod_threshold and pre < 2:
            print("2")
            pre = 2
        elif range_accel_shake > range_accel_nod and range_accel_shake > accel_shake_threshold and pre < 2:
            print("3")
            pre = 3
        elif pre >= 2 or (range_left < clench_threshold and range_right < clench_threshold):
            print("baseline")
            pre = -1
        elif range_left > range_right:
            print("0")
            pre = 0
        elif range_right > range_left:
            print("1")
            pre = 1

    board.stop_stream()
    board.release_session()


'''SAMPLING_RATE=125 #print("Sampling rate", BoardShim.get_sampling_rate(board_id))

# for i in range(30):
while True:
    time.sleep(0.1)
    current_data=board.get_current_board_data(SAMPLING_RATE) #does not remove from ring buffer. 256 samples
    eeg_channels=BoardShim.get_eeg_channels(board_id)
    lhs=0 #1-8
    cyton_scale_factor=0.02235
    ganglion_scale_factor=0.001869917138805
    rhs=0
    for channel in eeg_channels:
        DataFilter.perform_bandpass(current_data[channel], BoardShim.get_sampling_rate(board_id), 15.0, 50.0, 4, 'butterworth', 0)
        print(f"Channel {channel} is {np.mean(current_data[channel])}")
        if channel<=8:
            lhs+=np.mean(current_data[channel])
        else:
            rhs+=np.mean(current_data[channel])
        # channel_sums[channel]=np.mean(current_data[channel])
    
    lhs/=8
    rhs/=8

    print(f"Left side: {lhs}")
    print(f"Right side: {rhs}")

    # ML applications go here
    


board.stop_stream()
board.release_session()'''
