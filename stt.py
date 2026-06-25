import os
import streamlit as st 
from groq import Groq
from dotenv import load_dotenv
import time
load_dotenv()
api_key_resp=os.getenv("GROQ_API_KEY")
if not api_key_resp:
    try:
        api_key_resp = st.secrets["GROQ_API_KEY"]
    except:
        pass
client = Groq(api_key=api_key_resp)


def transcribe_audio(audio_bytes):
    if len(audio_bytes) < 10000:
        return None
    
    for attempt in range(3):  # 3 tries
        try:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio_bytes),
                model="whisper-large-v3-turbo",
                temperature=0,
                response_format="text"
            )
            return transcription
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            raise e