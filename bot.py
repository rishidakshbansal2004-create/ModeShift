import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
from config import MODES
import time
from google.genai import types
load_dotenv()

api_key_resp = os.getenv("Gem_Api_Key")

if not api_key_resp:
    try:
        api_key_resp = st.secrets["Gem_Api_Key"]
    except:
        pass
client1 = genai.Client(api_key=api_key_resp)


def create_chat_session(mode):
    chat=client.chats.create(
        model=mode["model"],
        config={"system_instruction":mode["system_prompt"]}
    )
    return chat

def call_with_retry(send_fn):
    for attempt in range(3):
        try:
            return send_fn()
        except Exception as e:
            if attempt <  2:
                time.sleep(2)
            else:
                raise e

def send_message(chat,message):
    start_time=time.time()
    response=call_with_retry(lambda: chat.send_message(message))
    latency=time.time()-start_time
    return {
        "text": response.text,
        "latency_seconds": round(latency, 2)
    }

def send_pdf(chat,pdf_upload,user_text="Here's my resume roast it"):
    start_time=time.time()
    response=call_with_retry(lambda: chat.send_message([types.Part.from_bytes(data=pdf_upload, mime_type="application/pdf"),
    user_text])
    )
    latency=time.time()-start_time
    return {
        "text": response.text,
        "latency_seconds": round(latency, 2)
    }