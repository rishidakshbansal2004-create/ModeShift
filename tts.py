import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def text_to_speech(text):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # George — professional male voice
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128"
    )
    
    audio_bytes = b"".join(audio)
    return audio_bytes