from flask import Flask, redirect
from flask_sock import Sock
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import time
import numpy as np
import json


app=Flask(__name__, static_folder='web', static_url_path='/')

@app.route('/')
def home():
    return redirect('/index.html')

sock=Sock(app)

@sock.route('/websocket')
def route(ws): #sends { type: letter | eeg, data: {} | '' }
    # https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
    board_id=BoardIds.CYTON_DAISY_BOARD.value #2 #CYTON_DAISY_BOARD
    params=BrainFlowInputParams()
    params.serial_port='/dev/cu.usbserial-DP05IK99'

    board = BoardShim(board_id, params)
    print("PRE")
    board.prepare_session()
    print("Successfully connected")
    board.start_stream()

    eeg_channels = BoardShim.get_eeg_channels(board_id)
    accel_channels = BoardShim.get_accel_channels(board_id)
    sampling_rate=board.get_sampling_rate(board_id)

    for i in range(3):
        time.sleep(1)
        data=board.get_board_data()
    time.sleep(1)
    baseline=board.get_board_data()
    # print("Set baseline to", baseline, type(baseline))

    while (True):
        time.sleep(1)
        data = board.get_board_data()

        arr_left = data[eeg_channels[1]]
        
        #mid = arr[int(0.25 * len(arr)):int(0.75 * len(arr))]
        #range_mid = np.ptp(mid)
        range_left = np.ptp(arr_left)

        arr_right = data[eeg_channels[9]]
        range_right = np.ptp(arr_right)
        
        if range_left < 200 and range_right < 200:
            print("baseline")
        elif range_left > range_right:
            print("0")
        elif range_right > range_left:
            print("1")

        channelToData={}
        for eeg_channel in eeg_channels:
            channelToData[eeg_channel]=np.mean(data[eeg_channel])-np.mean(baseline[eeg_channel])
        print(channelToData)
        ws.send(json.dumps({ 'type': 'eeg', 'data': channelToData }))

        '''
        accel = data[accel_channels[2]]
        range_accel = np.ptp(accel)
        if (range > 200):
            print("0")
        elif (range_accel > 0.14):
            print("1")
        else:
            print("baseline")'''
    
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
