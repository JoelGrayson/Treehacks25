import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
VOICE_ID=os.getenv('VOICE_ID')
API_KEY=os.getenv('API_KEY')
LUMA_API_KEY=os.getenv('LUMA_API_KEY')

def map_alpha_to_speech(alpha_value):
    """
    Maps alpha wave value (0 to 1) to TTS parameters.
    """
    if alpha_value > 0.7:  
        return {
            "stability": 0.9,   
            "similarity_boost": 0.3,
            "text_modifier": lambda text: text.lower() + "..."  
        }
    elif alpha_value > 0.4:  
        return {
            "stability": 0.6,
            "similarity_boost": 0.5,
            "text_modifier": lambda text: text  
        }
    else:
        return {
            "stability": 1.0,  
            "similarity_boost": 0.8,
            "text_modifier": lambda text: text.upper() + "!!!"  
        }

def generate_speech(text, alpha_value):
    params = map_alpha_to_speech(alpha_value)

    modified_text = params["text_modifier"](text)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": modified_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": params["stability"],
            "similarity_boost": params["similarity_boost"]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        with open("output_audio.mp3", "wb") as f:
            f.write(response.content)
        print("Audio saved as output_audio.mp3")
    else:
        print("Error:", response.text)

alpha_wave_value = 0.2
user_text = "You’re leaving?\" she asked, her voice trembling with sadness. \"That’s it!\" he exclaimed triumphantly."
generate_speech(user_text, alpha_wave_value)
