import edge_tts
import asyncio
import tempfile
import os

async def _generate(text, filename):
    communicate = edge_tts.Communicate(text, voice="en-IN-PrabhatNeural",rate="+25%")
    await communicate.save(filename)

def text_to_speech(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        filename = f.name
    asyncio.run(_generate(text, filename))
    with open(filename, "rb") as f:
        audio = f.read()
    os.unlink(filename)
    return audio