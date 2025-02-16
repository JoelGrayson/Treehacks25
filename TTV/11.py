import os
import requests
import random  # Replace with real EEG data source

# Configuration
VOICE_ID = "iP95p4xoKVk53GoZ742B"
API_KEY = "eleven-labs-api"

# Function to simulate EEG data (replace with actual BCI input)
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

def modify_text_based_on_eeg(text, eeg_data):
    """
    Modify text to upper case with excitement, lower case with boredom,
    or no change depending on EEG frequency values.
    """
    if eeg_data["gamma"] > 0.6:
        # High Gamma: Excitement
        modified_text = text.upper() + "!!!"
    elif eeg_data["theta"] > 0.6:
        # High Theta: Boredom
        modified_text = text.lower() + "..."
    else:
        # Balanced Signals: No Change
        modified_text = text
        
    print(f"Modified Text: {modified_text}")
    return modified_text

# Function to map EEG data to continuous voice parameters
def map_eeg_to_voice_params(eeg_data):
    # Style Exaggeration
    style_exaggeration = 0.5 + 1.5 * eeg_data["gamma"] + 0.5 * eeg_data["alpha"]
    style_exaggeration = min(max(style_exaggeration, 0.5), 2.0)  # Cap to natural range
    
    # Stability
    stability = 0.8 - 0.5 * eeg_data["beta"] - 0.3 * eeg_data["gamma"]
    stability = min(max(stability, 0.4), 1.0)  # Cap to natural range
    
    # Speed Factor
    speed_factor = 1.0 + 0.5 * eeg_data["gamma"] - 0.5 * eeg_data["theta"]
    speed_factor = min(max(speed_factor, 0.8), 1.5)  # Cap to natural range
    speed_ssml = f"{int(speed_factor * 100)}%"
    
    # Pitch Adjustment
    pitch_percent = (20 * eeg_data["gamma"]) - (20 * eeg_data["theta"])
    pitch_percent = min(max(pitch_percent, -20), 20)  # Cap to -20% to +20%
    pitch_adjustment = f"{pitch_percent:+.0f}%"
    
    print(f"Style Exaggeration: {style_exaggeration}")
    print(f"Stability: {stability}")
    print(f"Speed SSML: {speed_ssml}")
    print(f"Pitch Adjustment: {pitch_adjustment}")
    
    return style_exaggeration, stability, speed_ssml, pitch_adjustment

# Function to generate SSML text
def generate_ssml_text(speed_ssml, pitch_adjustment, text):
    return f"""
    <speak>
        <prosody rate="{speed_ssml}" pitch="{pitch_adjustment}">
            {text}
        </prosody>
    </speak>
    """

# Function to generate speech using ElevenLabs API
def generate_speech(ssml_text, style_exaggeration, stability):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": ssml_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": 0.8,
            "style_exaggeration": style_exaggeration,
            "use_speaker_boost": True
        },
        "text_type": "ssml"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("Speech generated and saved as output.mp3")
    except requests.exceptions.RequestException as e:
        print(f"Failed to generate speech: {e}")

# Main function
def main():
    delta, theta, alpha, beta, gamma = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
    text = "Hello I attend Stanford University and I am studying computer science."
    eeg_data = get_eeg_data(delta, theta, alpha, beta, gamma)
    modified_text = modify_text_based_on_eeg(text, eeg_data)
    style_exaggeration, stability, speed_ssml, pitch_adjustment = map_eeg_to_voice_params(eeg_data)
    ssml_text = generate_ssml_text(speed_ssml, pitch_adjustment, modified_text)
    generate_speech(ssml_text, style_exaggeration, stability)

if __name__ == "__main__":
    main()