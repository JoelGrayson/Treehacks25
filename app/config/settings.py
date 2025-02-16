from typing import Literal
from pydantic_settings import BaseSettings
from brainflow.board_shim import BoardIds


class Settings(BaseSettings):
    # App settings
    mode: Literal["inference", "collect", "simulate"] = "collect"

    # https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference
    # arrays in mV. DC offset 22.5mV. sample rate 125Hz
    board_id: int = BoardIds.CYTON_DAISY_BOARD.value
    serial_port: str = "/dev/cu.usbserial-DP05IK99"

    # Calibration thresholds
    # For Joe Li over-ear BCI, 12am
    accel_pitch_thres: float = 0.14
    accel_roll_thres: float = 0.14
    left_clench_thres: float = 500
    right_clench_thres: float = 350

    HOST: str = "0.0.0.0"
    PORT: int = 6969
    ENV: str = "development"

    # class Config:
    #     env_prefix = "BCI_"  # Environment variables will be prefixed with BCI_


# Create settings instance
settings = Settings()
