"""BCI client that reads from device and sends events via WebSocket."""

import websocket
import json
import time
import pickle
from pathlib import Path
from app.services.bci import bci_session, process_board_data, BCIParams
from app.config.settings import settings
from app.models import StateBit
from dataclasses import asdict
from tqdm import tqdm

# Simulation settings
SIMULATE = False  # Set to True to use pickle data instead of real device

params = BCIParams()


def loop_forever_bci(fetch_data, baseline, params, ws, delay):
    """Run BCI processing loop with configurable data source."""
    i = 0
    pbar = tqdm(unit=" bits")
    last_check = time.time()
    last_bit = StateBit.NOTHING

    while True:
        if time.time() - last_check < delay:
            continue

        event_data = process_board_data(fetch_data(i), baseline, params, last_bit)
        last_bit = event_data.bit
        # print(event_data.raw_data)
        if event_data.bit != StateBit.NOTHING:
            ws.send(json.dumps({"event": "bit", "data": asdict(event_data)}))
            pbar.update(1)
            pbar.set_postfix(bit=event_data.bit.value)
        else:
            pbar.set_postfix(bit="-1")
        i += 1
        last_check = time.time()


try:
    ws = websocket.WebSocket()
    ws.connect(f"ws://{settings.HOST}:{settings.PORT}/ws")
    if SIMULATE:
        with Path("eeg_data.pkl").open("rb") as f:
            data = pickle.load(f)
        loop_forever_bci(
            fetch_data=lambda i: data[i % len(data)],
            baseline=data[0],
            params=params,
            ws=ws,
            delay=0.1,
        )
    else:
        with bci_session(params) as board:
            baseline_data = board.get_board_data()
            loop_forever_bci(
                fetch_data=lambda _: board.get_board_data(),
                baseline=baseline_data,
                params=params,
                ws=ws,
                delay=1,
            )
finally:
    ws.abort()
    pass
    # if ws.connected:
    #     ws.close()
