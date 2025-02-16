import requests
import time
import random
from lumaai import LumaAI

client = LumaAI(
    auth_token="luma-auth-token"
)

def get_eeg_data(delta, theta, alpha, beta, gamma):
    eeg_data = {
        "delta": delta,
        "theta": theta,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma
    }
    
    # Normalize values to [0, 1]
    total_power = sum(eeg_data.values())
    if total_power > 0:
        eeg_data = {k: v / total_power for k, v in eeg_data.items()}
    
    print(f"EEG Data: {eeg_data}")
    return eeg_data

def generate_image(beta, prompt):
    if beta > 0.7:
        emotion_prompt = "neon / warm colors, high contrast, vibrant, cinematic lighting, highly energetic, excited, happy"
    elif beta > 0.4:
        emotion_prompt = "natural lighting, realistic color balance, neutral tones"
    else:
        emotion_prompt = "soft pastel colors, dreamy, soothing tones, low contrast, sadder / more monotone"
    
    generation = client.generations.image.create(
        prompt= prompt + emotion_prompt
    )

    completed = False
    while not completed:
        generation = client.generations.get(id=generation.id)
        if generation.state == "completed":
            completed = True
        elif generation.state == "failed":
            raise RuntimeError(f"Generation failed: {generation.failure_reason}")
        print("Dreaming")
        time.sleep(2)

    image_url = generation.assets.image

    # download the image
    response = requests.get(image_url, stream=True)
    with open(f'{generation.id}.jpg', 'wb') as file:
        file.write(response.content)
    print(f"File downloaded as {generation.id}.jpg")

delta, theta, alpha, beta, gamma = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
eeg_data = get_eeg_data(delta, theta, alpha, beta, gamma)
prompt = "A bear on a motorcycle dancing"
generate_image(eeg_data["beta"], prompt)