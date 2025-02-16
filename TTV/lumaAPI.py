import requests
LUMA_API_KEY = "your-luma-api-key"

def map_alpha_to_prompt(base_prompt, alpha_value):
    if alpha_value > 0.7: 
        return f"{base_prompt}, soft pastel colors, dreamy, soothing tones, low contrast"
    elif alpha_value > 0.4:
        return f"{base_prompt}, natural lighting, realistic color balance, warm tones"
    else: 
        return f"{base_prompt}, neon colors, high contrast, vibrant, cinematic lighting"

def generate_image_with_luma(prompt):
    url = "https://api.luma.com/v1/generate"  
    headers = {
        "Authorization": f"Bearer {LUMA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": prompt, "style": "cinematic"}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["image_url"]
    else:
        print("Error:", response.text)
        return None

alpha_wave_value = 0.3 
base_prompt = "A futuristic city at night"
modified_prompt = map_alpha_to_prompt(base_prompt, alpha_wave_value)
image_url = generate_image_with_luma(modified_prompt)

print("Generated Image URL:", image_url)
