from dataclasses import dataclass
from typing import Dict, Optional
import asyncio
from pathlib import Path
import requests
from lumaai import LumaAI

from app.config.settings import settings
from app.services.eleven import EEGData


@dataclass
class ImageGeneration:
    """Image generation result."""

    id: str
    state: str
    image_url: Optional[str] = None
    failure_reason: Optional[str] = None


class ImageService:
    """Image generation service with EEG-based prompt enhancement."""

    def __init__(self):
        self.client = LumaAI(auth_token=settings.LUMA_AI_AUTH_TOKEN)
        self.output_dir = Path("output/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _enhance_prompt(self, prompt: str, beta: float) -> str:
        """Enhance prompt based on beta wave intensity."""
        if beta > 0.7:
            emotion_prompt = (
                "neon / warm colors, high contrast, vibrant, "
                "cinematic lighting, highly energetic, excited, happy"
            )
        elif beta > 0.4:
            emotion_prompt = "natural lighting, realistic color balance, neutral tones"
        else:
            emotion_prompt = (
                "soft pastel colors, dreamy, soothing tones, "
                "low contrast, sadder / more monotone"
            )

        return f"{prompt} {emotion_prompt}"

    async def generate_image(self, prompt: str, eeg_data: EEGData) -> Path:
        """Generate an image based on prompt and EEG data."""
        normalized_eeg = eeg_data.normalize()
        enhanced_prompt = self._enhance_prompt(prompt, normalized_eeg["beta"])

        # Create generation using native client
        generation = self.client.generations.image.create(prompt=enhanced_prompt)

        # Poll for completion
        while True:
            generation = self.client.generations.get(id=generation.id)

            if generation.state == "completed":
                # Download the image
                output_path = self.output_dir / f"{generation.id}.jpg"
                response = requests.get(generation.assets.image, stream=True)
                response.raise_for_status()
                output_path.write_bytes(response.content)
                return output_path
            elif generation.state == "failed":
                raise RuntimeError(f"Generation failed: {generation.failure_reason}")

            await asyncio.sleep(2)


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    async def demo():
        """Demonstrate image generation with sample EEG data."""
        # Sample EEG data (high beta for vibrant images)
        eeg_data = EEGData(
            delta=0.1,
            theta=0.1,
            alpha=0.2,
            beta=0.8,  # High beta for vibrant/energetic style
            gamma=0.2,
        )

        service = ImageService()

        # Generate images with different prompts
        prompts = [
            "A futuristic brain-computer interface in a cyberpunk setting",
            "Neural networks visualized as a glowing constellation",
            "A peaceful zen garden with flowing water and cherry blossoms",
        ]

        for prompt in prompts:
            print(f"\nGenerating image for prompt: {prompt}")
            print("This may take a few minutes...")

            try:
                output_path = await service.generate_image(prompt, eeg_data)
                print(f"Generated image saved to: {output_path}")

                # Print the normalized EEG values used
                print("Normalized EEG values:")
                for band, value in eeg_data.normalize().items():
                    print(f"  {band}: {value:.2f}")
            except Exception as e:
                print(f"Error generating image: {e}")

    # Load environment variables and run demo
    load_dotenv()
    asyncio.run(demo())
