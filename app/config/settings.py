from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from brainflow.board_shim import BoardIds
from pathlib import Path

import os

PROJECT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # API Keys
    ELEVEN_LABS_API_KEY: str
    ELEVEN_LABS_VOICE_ID: str = "iP95p4xoKVk53GoZ742B"
    LUMA_AI_AUTH_TOKEN: str

    # Service Configuration
    ENABLE_TTS: bool = True
    ENABLE_IMAGE_GEN: bool = True

    # Voice Settings
    DEFAULT_STABILITY: float = 0.8
    DEFAULT_SIMILARITY_BOOST: float = 0.8
    DEFAULT_STYLE_EXAGGERATION: float = 0.5

    # Model Configuration
    TTS_MODEL_ID: str = "eleven_multilingual_v2"

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
    ENV: str = "production"

    class Config:
        dev_env_files = [
            os.path.join(PROJECT_DIR, ".env"),
            os.path.join(PROJECT_DIR, ".env.development"),
        ]

        env_file = (
            dev_env_files
            if os.environ.get("ENV", "development") == "development"
            else [dev_env_files[0]]
        )
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
