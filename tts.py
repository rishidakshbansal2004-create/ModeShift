import os
import streamlit as st
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
api_key_resp=os.getenv("ELEVENLABS_API_KEY")
if not api_key_resp:
    try:
        api_key_resp = st.secrets["ELEVENLABS_API_KEY"]
    except:
        pass
client = ElevenLabs(api_key=api_key_resp)

def text_to_speech(text):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # George — professional male voice
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128"
    )
    
    audio_bytes = b"".join(audio)
    return audio_bytes