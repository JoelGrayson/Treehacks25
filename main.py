# brainflow, numpy, matplotlib

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import matplotlib.pyplot as plt
import time

# brainflow, numpy, matplotlib

from brainflow.board_shim import BoardShim

# https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
board_id=2 #CYTON_DAISY_BOARD


params=BrainFlowInputParams()
# params.serial_port=

# https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
# CYTON_DAISY_BOARD=2


# find from ls /dev/.*
serial_port='/dev/ttyUSB0'
# '/dev/tty.usbserial-DP05IK99'

# tty.usbserial-DP05IK99
# params.serial_port = '/dev/cu.usbserial-DP05IK99'  # Update this line
params.serial_port = '/dev/tty.usbserial-DP05IK99'

# https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
# CYTON_DAISY_BOARD = 2

# find from ls /dev/.*
# serial_port = '/dev/cu.usbserial-DP05IK99'  # Update this line

try:
    board=BoardShim(board_id, params)
    board.prepare_session()
except Exception as e:
    print("Problem", e)
print("Prepared")
