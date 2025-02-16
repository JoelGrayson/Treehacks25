"""BCI client that reads from device and sends events via WebSocket."""

import websocket
import json
import time
import pickle
import numpy as np
from pathlib import Path
from app.services.bci import bci_session, process_board_data, BCIParams
from app.config.settings import settings
from app.models import StateBit
from dataclasses import asdict
from tqdm import tqdm

# Simulation settings
SIMULATE = True  # Set to True to use pickle data instead of real device

params = BCIParams(
    serial_port=settings.serial_port,
    board_id=settings.board_id,
    accel_pitch_thres=settings.accel_pitch_thres,
    accel_roll_thres=settings.accel_roll_thres,
    clench_thres=settings.clench_thres,
)

ws = websocket.WebSocket()
ws.connect(f"ws://{settings.HOST}:{settings.PORT}/ws")

if SIMULATE:
    with Path("eeg_data.pkl").open("rb") as f:
        sim_data = pickle.load(f)
        print(len(sim_data))
    sim_idx = 0

    # TODO: Sim broken spams 1. Assume works, then?

    pbar = tqdm(unit=" bits")
    last_check = time.time()
    while True:
        if time.time() - last_check < 0.1:
            continue

        data = sim_data[sim_idx % len(sim_data)]
        bit_event = process_board_data(data, sim_data[0], params)

        if bit_event.bit != StateBit.NOTHING:
            ws.send(json.dumps({"event": "bit", "data": asdict(bit_event)}))
            pbar.update(1)
            pbar.set_postfix(bit=bit_event.bit.value)

        sim_idx += 1
        last_check = time.time()
else:
    with bci_session(params) as board:
        baseline_data = board.get_board_data()

        while True:
            data = board.get_board_data()
            bit_event = process_board_data(data, baseline_data, params)

            if bit_event.bit != StateBit.NOTHING:
                ws.send(
                    json.dumps(
                        {
                            "event": "bit",
                            "data": asdict(bit_event),
                        }
                    )
                )
