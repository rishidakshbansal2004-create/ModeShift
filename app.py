import streamlit as st
from config import MODES, MODEL_NAME
from bot import create_chat_session, send_message, send_pdf
from audio_recorder_streamlit import audio_recorder
from stt import transcribe_audio
from tts import text_to_speech

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = None

if "chat" not in st.session_state:
    st.session_state.chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "first_time" not in st.session_state:
    st.session_state.first_time=None

if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

def switch_mode(new_mode_key):
    st.session_state.selected_mode = new_mode_key
    st.session_state.chat = None
    st.session_state.messages = []
    st.session_state.first_time=None
    st.session_state.last_audio=None
    st.rerun()
st.set_page_config(page_title="ModeShift", page_icon="🚀")
mode_greetings = {
    "interviewer": "🧑‍🏫 I'm your Mock Interviewer. Tell me your role and experience level, and let's begin!",
    "debugger": "🧑‍🔬 I'm your Code Debugger. Paste your buggy code (and any errors you're seeing) — let's squash it!",
    "resume_roast": "🎭 I'm here to Roast&Boost your resume. Upload your PDF and brace yourself! 🔥",
    "casual": "🙋 Hey, I'm your Friendly Neighbourhood Bot. What's on your mind today?",
}
with st.sidebar:
    st.title("🚀 ModeShift")
    st.caption("Your personal AI assistant — one bot, four personalities.")
    
    st.divider()
    
    st.subheader("🧭 Switch Mode")
    
    if st.button("🎤 Mock Interviewer", use_container_width=True):
        switch_mode("interviewer")
        
    
    if st.button("🐛 Code Debugger", use_container_width=True):
        switch_mode("debugger")
        
    
    if st.button("🎯 Roast&Boost My Resume", use_container_width=True):
        switch_mode("resume_roast")
        
    
    if st.button("😄 Friendly Neighbourhood Bot", use_container_width=True):
        switch_mode("casual")
        


if st.session_state.selected_mode is None:
    # ---- LANDING PAGE ----
    st.title("🚀 Welcome to ModeShift")
    st.write("✨ Your personal AI assistant")
    st.info("select a mode to dive in my 4 different personalities")
    st.divider()
    
    # mode buttons will go here (next step)
    mode_options = {
        "🎤 Mock Interviewer": "interviewer",
        "🐛 Code Debugger": "debugger",
        "🎯 Roast&Boost My Resume": "resume_roast",
        "😄 Friendly Neighbourhood Bot": "casual",
    }

    mode_descriptions = {
        "interviewer": "Practice technical & HR interviews with real-time feedback.",
        "debugger": "Paste broken code and get a senior dev's diagnosis.",
        "resume_roast": "Brutally funny, genuinely useful resume feedback.",
        "casual": "Just here to chat, vent, or hang out.",
    }
    selected_label = st.selectbox("Choose a mode:", list(mode_options.keys()))
    selected_key = mode_options[selected_label]

    st.caption(mode_descriptions[selected_key])

    if st.button("Let's Start ➡️"):
        switch_mode(selected_key)
        
else:
    # ---- CHAT PAGE ----
    mode_info = MODES[st.session_state.selected_mode]
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(mode_info["label"])
        st.write(mode_greetings[st.session_state.selected_mode])
    with col2:
        if st.button("🔄 Restart"):
            switch_mode(st.session_state.selected_mode)

    if st.session_state.chat is None:
        st.session_state.chat = create_chat_session(mode_info)

    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

     # ---- MOCK INTERVIEWER — VOICE MODE ----
    if st.session_state.selected_mode == "interviewer":
        if st.session_state.get("last_audio"):
            st.audio(st.session_state.last_audio, format="audio/mp3", autoplay=True)

        if st.session_state.first_time is None:
            st.info("⚠️ First time: Allow mic permission, then click mic AGAIN to record.")
            st.session_state.first_time="first time"
        st.write("🎙️ Press the mic and speak your answer and click it again to Send:")
        st.info("RED MEANS RECORDING")
    # Pehle audio play karo agar hai
        audio_bytes = audio_recorder(pause_threshold=3.0)
       
        if audio_bytes and audio_bytes !=st.session_state.last_processed:
            st.session_state.last_processed=audio_bytes
            with st.spinner("Brace yourself feedback/next question is coming shortly"):
                with st.spinner("🎙️ Processing your answer..."):
                    user_text = transcribe_audio(audio_bytes)
        
                if user_text is None:
                    st.warning("Recording too short — please try again!")
                    st.stop()
        
                st.session_state.messages.append({"role": "user", "content": user_text})
        
                with st.spinner("🧑‍🏫 Interviewer is thinking..."):
                    result = send_message(st.session_state.chat, user_text)
        
                st.session_state.messages.append({"role": "assistant", "content": result["text"]})
        
                with st.spinner("🔊 Preparing response..."):
                    audio_output = text_to_speech(result["text"])
        
                st.session_state.last_audio = audio_output
                st.rerun()
   
    elif st.session_state.selected_mode == "resume_roast" :
        user_input = st.chat_input("Type a message or attach your resume PDF...",accept_file=True,file_type=["pdf"])
        if user_input:
            if user_input.files:
                uploaded_file = user_input.files[0]
                pdf_upload = uploaded_file.read()

                with st.chat_message("user"):
                    st.write(f"📄 Uploaded: {uploaded_file.name}")
                st.session_state.messages.append({"role": "user", "content": f"📄 Uploaded: {uploaded_file.name}"})

                with st.spinner("Reading your resume... brace yourself 🔥"):
                    result = send_pdf(st.session_state.chat, pdf_upload)
                    st.caption(f"⚡ {result['latency_seconds']}s")

                with st.chat_message("assistant"):
                    st.write(result["text"])
                st.session_state.messages.append({"role": "assistant", "content": result["text"]})   
            elif user_input.text:
                with st.chat_message("user"):
                    st.write(user_input.text)
                st.session_state.messages.append({"role": "user", "content": user_input.text})

                with st.spinner("Roast incoming..."):
                    result = send_message(st.session_state.chat, user_input.text)
                    st.caption(f"⚡ {result['latency_seconds']}s")
                with st.chat_message("assistant"):
                    st.write(result["text"])
                st.session_state.messages.append({"role": "assistant", "content": result["text"]})
                 

    else:
        user_input = st.chat_input("Type your message...")
        # process as normal text message — same as your existing flow

        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Analyzing your Input"):
                result = send_message(st.session_state.chat, user_input)

            with st.chat_message("assistant"):
                st.write(result["text"])
                st.caption(f"⚡ {result['latency_seconds']}s")
            st.session_state.messages.append({"role": "assistant", "content": result["text"]})