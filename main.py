from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
# from brainflow.data_filter import DataFilter, FilterTypes
import time

# https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
board_id=BoardIds.CYTON_DAISY_BOARD.value #2 #CYTON_DAISY_BOARD
params=BrainFlowInputParams()
params.serial_port = '/dev/cu.usbserial-DP05IK99'

board=BoardShim(board_id, params)
board.prepare_session()
board.start_stream()
# time.sleep(5)
# data=board.get_board_data()

# for i in range(1000):

# About brainflow data as microvolts

while True:
    time.sleep(0.1)
    current_data=board.get_current_board_data(25)
    print(current_data)

board.stop_stream()
board.release_session()

