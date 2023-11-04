import os

from elevenlabs import Voice, VoiceSettings, generate
from elevenlabs import set_api_key
from dotenv import load_dotenv
from elevenlabs import play
load_dotenv()


import requests

url = "https://api.elevenlabs.io/v1/models/"

headers = {
  "Accept": "application/json",
  "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
}

response = requests.get(url, headers=headers)

print(response.text)


exit()

set_api_key(os.getenv("ELEVENLABS_API_KEY"))
audio = generate(
    text="Hello! My name is Bella.",
    voice=Voice(
        voice_id='EXAVITQu4vr4xnSDxMaL',
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    )
)
play(audio)