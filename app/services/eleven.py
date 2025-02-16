from dataclasses import dataclass
from typing import Dict, Tuple
import aiohttp
import asyncio
from pathlib import Path

from app.config.settings import settings


@dataclass
class EEGData:
    """EEG frequency band data."""

    delta: float
    theta: float
    alpha: float
    beta: float
    gamma: float

    def normalize(self) -> Dict[str, float]:
        """Normalize values to sum to 1."""
        total = sum([self.delta, self.theta, self.alpha, self.beta, self.gamma])
        if total <= 0:
            return {k: 0.0 for k in ["delta", "theta", "alpha", "beta", "gamma"]}
        return {
            "delta": self.delta / total,
            "theta": self.theta / total,
            "alpha": self.alpha / total,
            "beta": self.beta / total,
            "gamma": self.gamma / total,
        }


@dataclass
class VoiceParameters:
    """Voice modification parameters based on EEG data."""

    style_exaggeration: float
    stability: float
    speed_ssml: str
    pitch_adjustment: str


class TTSService:
    """Text-to-Speech service with EEG-based voice modulation."""

    def __init__(self):
        self.api_key = settings.ELEVEN_LABS_API_KEY
        self.voice_id = settings.ELEVEN_LABS_VOICE_ID
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def modify_text(self, text: str, eeg_data: Dict[str, float]) -> str:
        """Modify text based on EEG frequency bands."""
        if eeg_data["gamma"] > 0.6:
            return text.upper() + "!!!"
        elif eeg_data["theta"] > 0.6:
            return text.lower() + "..."
        return text

    def map_eeg_to_voice_params(self, eeg_data: Dict[str, float]) -> VoiceParameters:
        """Map EEG data to voice parameters."""
        # Style Exaggeration
        style_exaggeration = 0.5 + 1.5 * eeg_data["gamma"] + 0.5 * eeg_data["alpha"]
        style_exaggeration = min(max(style_exaggeration, 0.5), 2.0)

        # Stability
        stability = 0.8 - 0.5 * eeg_data["beta"] - 0.3 * eeg_data["gamma"]
        stability = min(max(stability, 0.4), 1.0)

        # Speed Factor
        speed_factor = 1.0 + 0.5 * eeg_data["gamma"] - 0.5 * eeg_data["theta"]
        speed_factor = min(max(speed_factor, 0.8), 1.5)
        speed_ssml = f"{int(speed_factor * 100)}%"

        # Pitch Adjustment
        pitch_percent = (20 * eeg_data["gamma"]) - (20 * eeg_data["theta"])
        pitch_percent = min(max(pitch_percent, -20), 20)
        pitch_adjustment = f"{pitch_percent:+.0f}%"

        return VoiceParameters(
            style_exaggeration=style_exaggeration,
            stability=stability,
            speed_ssml=speed_ssml,
            pitch_adjustment=pitch_adjustment,
        )

    def generate_ssml(self, text: str, voice_params: VoiceParameters) -> str:
        """Generate SSML markup for voice modification."""
        return f"""
        <speak>
            <prosody rate="{voice_params.speed_ssml}" pitch="{voice_params.pitch_adjustment}">
                {text}
            </prosody>
        </speak>
        """

    async def generate_speech(
        self, ssml_text: str, voice_params: VoiceParameters
    ) -> Path:
        """Generate speech using ElevenLabs API."""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}

        payload = {
            "text": ssml_text,
            "model_id": settings.TTS_MODEL_ID,
            "voice_settings": {
                "stability": voice_params.stability,
                "similarity_boost": settings.DEFAULT_SIMILARITY_BOOST,
                "style_exaggeration": voice_params.style_exaggeration,
                "use_speaker_boost": True,
            },
            "text_type": "ssml",
        }

        output_path = self.output_dir / f"speech_{asyncio.get_event_loop().time()}.mp3"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                content = await response.read()
                output_path.write_bytes(content)

        return output_path

    async def process_text(self, text: str, eeg_data: EEGData) -> Path:
        """Process text with EEG data and generate speech."""
        normalized_eeg = eeg_data.normalize()
        modified_text = self.modify_text(text, normalized_eeg)
        voice_params = self.map_eeg_to_voice_params(normalized_eeg)
        ssml_text = self.generate_ssml(modified_text, voice_params)
        return await self.generate_speech(ssml_text, voice_params)


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    async def demo():
        """Demonstrate TTS service with sample EEG data."""
        # Sample EEG data (high gamma for excitement)
        eeg_data = EEGData(
            delta=0.1,
            theta=0.1,
            alpha=0.2,
            beta=0.2,
            gamma=0.8,  # High gamma for excitement
        )

        service = TTSService()

        # Process multiple sample texts with different emotional content
        texts = [
            "I am so excited about this project!",
            "The neural interface is working perfectly.",
            "Brain waves are being processed in real-time.",
        ]

        for text in texts:
            print(f"\nProcessing text: {text}")
            output_path = await service.process_text(text, eeg_data)
            print(f"Generated audio saved to: {output_path}")

            # Print the normalized EEG values used
            print("Normalized EEG values:")
            for band, value in eeg_data.normalize().items():
                print(f"  {band}: {value:.2f}")

    # Load environment variables and run demo
    load_dotenv()
    asyncio.run(demo())
