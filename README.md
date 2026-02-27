# LangTeach · AI Language Tutor

> A conversational AI language tutor powered by **Groq LLaMA 3.3**, **Whisper**, and **Edge-TTS** — served as a self-contained Docker app.

---

## ✨ Features

- 🧠 **Curriculum-aware tutoring** — structured syllabi for Italian, French, and English (A1–B2), with grammar, vocabulary, conversation and cultural content per level
- 🎯 **Intelligent error correction** — corrections are embedded naturally in the conversation and displayed as pedagogical notes
- 🗣️ **Voice input** — record audio directly in the browser, transcribed via Groq Whisper
- 🔊 **Text-to-speech output** — responses are spoken in the target language (Edge-TTS); corrections are spoken in the student's native language
- 📊 **Session progress tracking** — turn count, score, error log, and level progress bar
- 🌍 **Multi-language support** — 10 target languages, 5 native languages
- 🔑 **Server-side API key** — configure `GROQ_API_KEY` in `.env` so users don't need to provide their own
- 🐳 **Docker-first** — one command deploy with `deploy.ps1`

---

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac/Linux)
- A [Groq API key](https://console.groq.com) (free tier available)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/language_teacher.git
cd language_teacher
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_key_here
```

> If `GROQ_API_KEY` is set, the API key field in the UI is hidden automatically — users can start learning immediately.

### 3. Deploy

```powershell
.\deploy.ps1
```

Open your browser at **http://localhost:8000**

---

## 🐳 Docker Deploy Script

[`deploy.ps1`](deploy.ps1) handles the full Docker lifecycle:

| Command | Description |
|---|---|
| `.\deploy.ps1` | Deploy with layer cache (fast) |
| `.\deploy.ps1 -Rebuild` | Full rebuild, no cache |
| `.\deploy.ps1 -NoCache` | Build without cache |
| `.\deploy.ps1 -Logs` | Tail container logs after deploy |
| `.\deploy.ps1 -Stop` | Stop and remove the container |
| `.\deploy.ps1 -Clean` | Remove container + image |
| `.\deploy.ps1 -Port 9000` | Deploy on a custom port (default: 8000) |

The script:
1. Verifies Docker Desktop is running
2. Reads `.env` and passes it to the container with `--env-file`
3. Builds the image (skipped if already exists, unless `-Rebuild`)
4. Starts the container with `--restart unless-stopped`
5. Runs a health check — polls `/` up to 12 times (3s interval)

---

## 🗂️ Project Structure

```
language_teacher/
├── .env                        # GROQ_API_KEY (git-ignored)
├── Dockerfile
├── deploy.ps1                  # Windows deploy script
├── requirements.txt
└── src/
    ├── app.py                  # FastAPI application (API endpoints)
    ├── config.py               # Languages, levels, defaults, language registry
    ├── utils.py                # Groq client, LLM calls, TTS, transcription
    ├── prompts/
    │   ├── prompts.py          # System prompt builder, intro message
    │   ├── english.py          # English curriculum & config
    │   ├── french.py           # French curriculum & config
    │   └── italian.py          # Italian curriculum & config
    └── static/
        └── style.html          # Single-file frontend (HTML + CSS + JS)
```

---

## 🔌 API Reference

All endpoints are served by FastAPI at `http://localhost:8000`.

### `GET /api/config`
Returns available languages, levels, defaults, and whether the server has an API key configured.

```json
{
  "languages": { "Italiano": { "code": "it", "flag": "🇮🇹" }, ... },
  "levels":    { "A1": "Absolute beginner...", ... },
  "defaults":  { "language": "Italiano", "level": "A2", ... },
  "server_has_key": true
}
```

---

### `POST /api/init`
Fires the tutor's opening message for a new session.

**Request:**
```json
{
  "profile": { "language": "French", "level": "B1", "topic": "Ordering at a café", "native": "Spanish" },
  "api_key": ""
}
```

**Response:**
```json
{
  "intro_user":  "Hello, I'm your student...",
  "main":        "Bonjour! Je suis LangTeach...",
  "correction":  "",
  "note":        "Today we'll focus on...",
  "timestamp":   "14:32"
}
```

---

### `POST /api/chat`
Sends a student message and returns the tutor's response.

**Request:**
```json
{
  "message":  "Je veux aller au marché",
  "profile":  { "language": "French", "level": "A2", "topic": "Shopping", "native": "Spanish" },
  "progress": { "turns": 5, "errors": [], "vocab_seen": [], "score": 50 },
  "messages": [ ... ],
  "api_key":  ""
}
```

**Response:**
```json
{
  "main":       "Très bien! Tu veux aller au marché...",
  "correction": "Tip: 'vouloir' + infinitive expresses desire.",
  "note":       "Grammaire: vouloir + infinitif...",
  "timestamp":  "14:33"
}
```

---

### `POST /api/tts`
Returns combined audio: correction in the native language + response in the target language.

**Request:**
```json
{
  "text":             "Bonjour! Comment ça va?",
  "language":         "Francés",
  "native":           "Spanish",
  "speak_correction": true,
  "correction_text":  "Recuerda usar 'tu' con amigos."
}
```

**Response:**
```json
{ "audio_b64": "<base64 encoded mp3>" }
```

---

### `POST /api/transcribe`
Transcribes base64-encoded audio using Groq Whisper.

**Request:**
```json
{
  "audio_b64": "<base64 encoded webm>",
  "language":  "Francés",
  "api_key":   ""
}
```

**Response:**
```json
{ "text": "Je voudrais un café, s'il vous plaît." }
```

---

## 🧩 Adding a New Language

1. Create `src/prompts/<language>.py` with:
   - `<LANGUAGE>_CONFIG` — name, code, voice, phonetics, grammar focus, false friends, cultural notes, recommended media, and curriculum (A1–B2)
   - `<LANGUAGE>_SYSTEM_PROMPT_EXTRA` — language-specific teaching instructions for the LLM

2. Register it in [`src/config.py`](src/config.py):
```python
from prompts.german import GERMAN_CONFIG, GERMAN_SYSTEM_PROMPT_EXTRA

LANGUAGE_REGISTRY = {
    ...
    "German": {"config": GERMAN_CONFIG, "extra_prompt": GERMAN_SYSTEM_PROMPT_EXTRA},
}
```

3. Add the TTS voice and language code to the `LANGUAGES` dict in [`src/config.py`](src/config.py):
```python
LANGUAGES = {
    ...
    "Alemán": {"code": "de", "voice": "de-DE-KatjaNeural", "flag": "🇩🇪"},
}
```

4. Rebuild: `.\deploy.ps1 -Rebuild`

---

## 🤖 AI Model Details

| Component | Model | Provider |
|---|---|---|
| Conversation / Tutoring | `llama-3.3-70b-versatile` | Groq |
| Speech-to-Text | `whisper-large-v3` | Groq |
| Text-to-Speech | Edge-TTS (Microsoft Neural Voices) | Local |

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Your Groq API key. Get one free at [console.groq.com](https://console.groq.com) |

---

## 🛠️ Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
cd src
uvicorn app:app --reload --port 8000
```

Make sure `GROQ_API_KEY` is set in your `.env` file or exported as an environment variable.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | 0.111.0 | Web framework & API |
| `uvicorn[standard]` | 0.29.0 | ASGI server |
| `groq` | 0.9.0 | LLM + Whisper API client |
| `edge-tts` | 6.1.9 | Text-to-speech |
| `python-dotenv` | 1.0.0 | `.env` file loading |
| `pydub` | 0.25.1 | Audio processing |

---

## 📄 License

MIT License — feel free to fork, adapt, and deploy your own language tutor.