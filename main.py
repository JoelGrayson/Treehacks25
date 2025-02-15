# brainflow, numpy, matplotlib

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
# from brainflow.data_filter import DataFilter, FilterTypes
import time

# https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
board_id=BoardIds.CYTON_DAISY_BOARD.value #2 #CYTON_DAISY_BOARD
params=BrainFlowInputParams()
# find from ls /dev/.*
# params.serial_port = '/dev/tty.usbserial-DP05IK99'
params.serial_port = '/dev/cu.usbserial-DP05IK99'

try:
    print("PRE")
    board=BoardShim(board_id, params)
    print("B")
    board.prepare_session()
    print("Successfully connected")
    board.start_stream()
    print("Getting board data")
    time.sleep(5)
    data=board.get_board_data()
    board.stop_stream()
    board.release_session()
    board.get_eeg_channels(board_id)
    sampling_rate=board.get_sampling_rate(board_id)
#     print(data)
except Exception as e:
    print("Problem", e)
print("Prepared")

# board.release_session()

