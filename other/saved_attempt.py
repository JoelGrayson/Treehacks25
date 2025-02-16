from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
import time
import numpy as np

# https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
board_id=BoardIds.CYTON_DAISY_BOARD.value #2 #CYTON_DAISY_BOARD
params=BrainFlowInputParams()
params.serial_port='/dev/cu.usbserial-DP05IK99'

board=BoardShim(board_id, params)
board.prepare_session()
board.start_stream()

SAMPLING_RATE=125 #BoardShim.get_sampling_rate(board_id)

sampling_rate=BoardShim.get_sampling_rate(board_id)
eeg_channels=BoardShim.get_eeg_channels(board_id)
cyton_scale_factor=0.02235

while True:
    time.sleep(0.1)
    current_data=board.get_current_board_data(SAMPLING_RATE) #does not remove from ring buffer. 256 samples
    # lhs=0 #1-8
    # rhs=0
    for count, channel in enumerate(eeg_channels):
        # plot timeseries
        DataFilter.detrend(current_data[channel], 1) # 1 for DetrendOperations.CONSTANT.value
        DataFilter.perform_bandpass(current_data[channel], sampling_rate, 3.0, 45.0, 2,
                                    FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
        DataFilter.perform_bandstop(current_data[channel], sampling_rate, 48.0, 52.0, 2,
                                    FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
        DataFilter.perform_bandstop(current_data[channel], sampling_rate, 58.0, 62.0, 2,
                                    FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
        print(current_data[channel].tolist())


    # for channel in eeg_channels:
    #     DataFilter.perform_bandpass(current_data[channel], BoardShim.get_sampling_rate(board_id), 15.0, 50.0, 4, 'butterworth', 0)
    #     print(f"Channel {channel} is {np.mean(current_data[channel])}")
    #     if channel<=8:
    #         lhs+=np.mean(current_data[channel])
    #     else:
    #         rhs+=np.mean(current_data[channel])
    
    # lhs/=8
    # rhs/=8

    # print(f"Left side: {lhs}")
    # print(f"Right side: {rhs}")

    # ML applications go here
    


board.stop_stream()
board.release_session()

