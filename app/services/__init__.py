from typing import Optional
from functools import lru_cache

from app.config.settings import settings
from app.services.eleven import TTSService
from app.services.luma import ImageService


@lru_cache
def get_tts_service() -> Optional[TTSService]:
    """Get TTS service singleton if enabled."""
    if settings.ENABLE_TTS:
        return TTSService()
    return None


@lru_cache
def get_image_service() -> Optional[ImageService]:
    """Get image service singleton if enabled."""
    if settings.ENABLE_IMAGE_GEN:
        return ImageService()
    return None
