# 🚀 ModeShift

**Your personal AI assistant — one bot, four personalities.**

ModeShift is a multi-mode AI chatbot built on the Gemini API, where a single application switches between four distinct, purpose-built personas — each with its own system prompt, behavior rules, and dynamically assigned model. Rather than one generic chatbot, ModeShift is four small, focused applications sharing one well-engineered backend.

🔗 **Live Demo:** [modeshiftby-rishi.streamlit.app](https://modeshiftby-rishi.streamlit.app)

> ⏳ Note: the app is hosted on Streamlit Community Cloud's free tier, so it may take a little longer to load on first visit if it's been idle (cold start). Subsequent interactions are fast.

---

## 🎥 Demo

[![Watch the demo](https://img.youtube.com/vi/Bx9FLCjRE0A/maxresdefault.jpg)](https://youtube.com/watch?v=Bx9FLCjRE0A)

*A full walkthrough of all 4 modes — Mock Interviewer, Code Debugger, Roast&Boost My Resume, and Friendly Neighbourhood Bot. Click to watch.*

---

## ✨ Features

| Mode | What it does |
|---|---|
| 🎤 **Mock Interviewer** | Conducts a structured, one-question-at-a-time mock interview for any role, gives feedback after every answer (strength, weakness, ideal approach), and closes with an evidence-based final verdict. |
| 🐛 **Code Debugger** | Diagnoses bugs in pasted code — logic errors, syntax errors, edge cases, runtime exceptions — and returns structured, snippet-level fixes without rewriting the whole file. |
| 🎯 **Roast&Boost My Resume** | Upload a resume PDF and get a brutally funny, emoji-heavy roast — paired with genuinely actionable, specific fixes for every section. |
| 😄 **Friendly Neighbourhood Bot** | A warm, casual conversational companion that mirrors the user's emotional tone, with built-in boundaries for sensitive topics and region-agnostic crisis-resource handling. |

---

## 🧠 Why Different Models Per Mode?

Each mode uses a different Gemini model, deliberately chosen based on the reasoning complexity the task demands rather than defaulting to one model everywhere:

| Mode | Model | Why |
|---|---|---|
| Mock Interviewer | `gemini-2.5-flash` | Judgment-heavy (evaluating answer quality, tracking conversation state for a final verdict) but doesn't need top-tier agentic/coding strength. |
| Code Debugger | `gemini-3.5-flash` | Strongest available reasoning — needed to catch subtle, multi-step bugs (e.g. operator precedence, memory allocation errors) reliably. |
| Roast&Boost My Resume | `gemini-3.5-flash` | Leans on tone/creativity with  deep multi-step reasoning for judgment; Needs model which supports file upload 
| Friendly Neighbourhood Bot | `gemini-3.1-flash-lite` | Lightweight conversational matching — no complex reasoning required. |

This split was validated through direct side-by-side testing during development (see [`/docs`](#) for sample comparisons) rather than assumed.

---

## ⚡ Performance & Reliability

| Metric | Detail |
|---|---|
| Avg. latency — Mock Interviewer | ~2.1s |
| Avg. latency — Code Debugger | ~5.1s |
| Avg. latency — Casual Chat | ~1.2s |
| Avg. latency — Resume Roast (PDF input) | ~12.3s |
| Retry handling | Up to 3 automatic retries on transient API failures, with a short backoff between attempts |
| Est. cost per full session | ₹3–4 ($0.04) on the highest-tier model used; lighter modes cost a fraction of that |

Latency is measured and surfaced live in the UI for every response, not just benchmarked separately — the app tracks its own performance as it runs.

---

## 🏗️ Architecture

```
ModeShift/
├── app.py              # Streamlit UI — landing page, sidebar, chat interface
├── bot.py               # Gemini API logic — chat sessions, retry handling, PDF input
├── config.py             # Mode definitions: system prompts + per-mode model assignment
├── .streamlit/
│   └── config.toml        # Dark theme configuration
├── .env                  # API key (not committed)
└── requirements.txt
```

**Design decisions worth noting:**
- **Per-mode chat sessions** — switching modes starts a completely fresh conversation (no cross-mode context bleed), implemented via a single `switch_mode()` helper that resets session state cleanly.
- **Multimodal PDF input** — resumes are sent directly to Gemini as raw PDF bytes (not pre-extracted text), preserving layout and formatting context that matters for presentation feedback.
- **Unified chat input for Resume Roast** — text and PDF attachment share a single `st.chat_input(accept_file=True)` box, so the user can roast a resume and ask follow-up questions through the same interface.
- **Generic retry wrapper** — `call_with_retry()` wraps any API call (text or PDF) uniformly, rather than duplicating retry logic per call type.

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **LLM:** Google Gemini API (`google-genai` SDK)
- **Models used:** `gemini-2.5-flash`, `gemini-3.5-flash`, `gemini-3.1-flash-lite`
- **Language:** Python 3.12

---

## 📦 Installation

### Prerequisites
- Python 3.10–3.13
- A Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/ModeShift.git
cd ModeShift
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your API key**

Create a `.env` file in the project root:
```bash
touch .env
```

Add your Gemini API key inside it:
```
GEMINI_API_KEY=your_api_key_here
```

**5. Run the app**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🚀 Usage

1. On launch, select a mode from the dropdown on the landing page (or use the sidebar anytime to switch).
2. **Mock Interviewer:** State your target role and experience level to begin. Type `next` only when you're ready to move past feedback to the next question.
3. **Code Debugger:** Paste your code (and any error messages, if you have them) directly into the chat.
4. **Roast&Boost My Resume:** Attach your resume PDF using the 📎 icon in the chat input.
5. **Friendly Neighbourhood Bot:** Just start chatting.
6. Use the **🔄 Restart** button (top-right of any chat) to reset the current mode's conversation at any time.

---

## 🔮 Future Improvements

- [ ] Streaming responses (word-by-word output) — deferred intentionally, since it complicates retry-on-failure handling; planned as a separate, focused addition
- [ ] Per-mode accent colors in the UI, layered on top of the current dark theme
- [ ] Persistent latency/usage logging for richer performance analytics over time
- [ ] Deployment to Streamlit Community Cloud

---

## 📄 License

This project is for educational and portfolio purposes.

---

*Built by Rishi Bansal — Computer Science undergraduate at IIIT Kottayam, specializing in Generative AI and Prompt Engineering.*
