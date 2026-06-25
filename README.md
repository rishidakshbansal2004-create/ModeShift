# 🚀 ModeShift

**Your personal AI assistant — one bot, four personalities.**

ModeShift is a multi-mode AI chatbot built on the Gemini API, where a single application switches between four distinct, purpose-built personas — each with its own system prompt, behavior rules, and dynamically assigned model. Rather than one generic chatbot, ModeShift is four small, focused applications sharing one well-engineered backend.

🔗 **Live Demo:** [modeshiftby-rishi.streamlit.app](https://modeshiftby-rishi.streamlit.app)

> ⏳ Note: the app is hosted on Streamlit Community Cloud's free tier, so it may take a little longer to load on first visit if it's been idle (cold start). Subsequent interactions are fast.

---

## 🎥 Demo

[![Watch the demo](https://img.youtube.com/vi/Bx9FLCjRE0A/maxresdefault.jpg)](https://youtube.com/watch?v=Bx9FLCjRE0A)

*A full walkthrough of all 4 modes. Click to watch.*

---

## ✨ Features

| Mode | What it does |
|---|---|
| 🎤 **Mock Interviewer** | Conducts a structured, one-question-at-a-time voice-driven mock interview. Speak your answer via mic, get feedback after every response, and close with a final verdict. Powered by Groq Whisper STT and edge TTS with auto-play responses. |
| 🐛 **Code Debugger** | Diagnoses bugs in pasted code — logic errors, syntax errors, edge cases, runtime exceptions — and returns structured, snippet-level fixes without rewriting the whole file. |
| 🎯 **Roast&Boost My Resume** | Upload a resume PDF and get a brutally funny, emoji-heavy roast paired with genuinely actionable, specific fixes for every section. |
| 😄 **Friendly Neighbourhood Bot** | A warm, casual conversational companion that mirrors the user's emotional tone, with built-in boundaries for sensitive topics and region-agnostic crisis-resource handling. |

---

## 🧠 Why Different Models Per Mode?

Each mode uses a different Gemini model, deliberately chosen based on the reasoning complexity the task demands:

| Mode | Model | Why |
|---|---|---|
| Mock Interviewer | `gemini-2.5-flash` | Judgment-heavy but doesn't need top-tier agentic strength. |
| Code Debugger | `gemini-3.5-flash` | Strongest available reasoning for subtle multi-step bugs. |
| Roast&Boost My Resume | `gemini-3.5-flash` | Tone/creativity with deep multi-step reasoning; supports file upload. |
| Friendly Neighbourhood Bot | `gemini-3.1-flash-lite` | Lightweight conversational matching, no complex reasoning required. |

This split was validated through direct side-by-side testing during development.

---

## ⚡ Performance & Reliability

| Metric | Detail |
|---|---|
| Avg. latency — Mock Interviewer | ~8.1s |
| Avg. latency — Code Debugger | ~5.1s |
| Avg. latency — Casual Chat | ~1.2s |
| Avg. latency — Resume Roast (PDF input) | ~12.3s |
| Retry handling | Up to 3 automatic retries on transient API failures with short backoff |
| Est. cost per full session | ~₹3-4 ($0.04) on highest-tier model; lighter modes cost a fraction |

---

## 🏗️ Architecture

```
ModeShift/
├── app.py              # Streamlit UI — landing page, sidebar, chat interface
├── bot.py              # Gemini API logic — chat sessions, retry handling, PDF input
├── config.py           # Mode definitions: system prompts + per-mode model assignment
├── stt.py              # Groq Whisper STT — mic audio to text transcription
├── tts.py              # edge TTS — text to voice with auto-play
├── .streamlit/
│   └── config.toml     # Dark theme configuration
├── .env                # API keys (not committed)
└── requirements.txt
```

**Design decisions worth noting:**
- **Voice-driven Mock Interviewer** — mic input transcribed via Groq Whisper, responses auto-played via ElevenLabs TTS, with silence detection and persistent chat history.
- **Per-mode chat sessions** — switching modes starts a completely fresh conversation, implemented via a single `switch_mode()` helper that resets session state cleanly.
- **Multimodal PDF input** — resumes sent directly to Gemini as raw PDF bytes, preserving layout context.
- **Unified chat input for Resume Roast** — text and PDF attachment share a single `st.chat_input(accept_file=True)` box.
- **Generic retry wrapper** — `call_with_retry()` wraps any API call uniformly, no duplicate retry logic.

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **LLM:** Google Gemini API (`google-genai` SDK)
- **STT:** Groq Whisper (`whisper-large-v3-turbo`)
- **TTS:** Edge Tts
- **Models used:** `gemini-2.5-flash`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`
- **Language:** Python 3.12

---

## 📦 Installation

### Prerequisites
- Python 3.10–3.13
- Gemini API key ([get one here](https://aistudio.google.com/apikey))
- Groq API key ([get one here](https://console.groq.com))
- ElevenLabs API key ([get one here](https://elevenlabs.io))

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/rishidakshbansal2004-create/ModeShift.git
cd ModeShift
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your API keys**

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

**5. Run the app**
```bash
streamlit run app.py
```

---

## 🚀 Usage

1. Select a mode from the dropdown on the landing page or sidebar.
2. **Mock Interviewer:** State your role and experience level. Speak your answers via mic — the interviewer responds with voice automatically.
3. **Code Debugger:** Paste your code and any error messages directly into chat.
4. **Roast&Boost My Resume:** Attach your resume PDF using the 📎 icon.
5. **Friendly Neighbourhood Bot:** Just start chatting.
6. Use **🔄 Restart** to reset the current mode anytime.

---

## 🔮 Future Improvements

- [ ] Streaming responses — deferred intentionally, complicates retry handling; planned as a separate addition
- [ ] Per-mode accent colors in UI
- [ ] Persistent latency/usage logging for richer performance analytics
- [ ] Voice support for additional modes beyond Mock Interviewer

---

## 📄 License

This project is for educational and portfolio purposes.

---

*Built by Rishi Bansal — Computer Science undergraduate at IIIT Kottayam, specializing in Generative AI, RAG pipelines, and AI Agents.*
