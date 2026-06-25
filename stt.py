import os
from groq import Groq
from dotenv import load_dotenv
import time
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


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