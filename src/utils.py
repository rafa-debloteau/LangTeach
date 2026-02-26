import asyncio
import base64
import json
import logging
import tempfile
from datetime import datetime
from typing import Optional, Tuple
import streamlit as st

import edge_tts
from groq import Groq

from config import *
from prompts import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_client(api_key: str) -> Optional[Groq]:
    """Creates a Groq client with error handling."""
    if not api_key:
        logging.warning("API key not provided.")
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        logging.error(f"Failed to create Groq client: {e}")
        return None

def call_llm(client: Groq, user_message: str, profile: dict, progress: dict, messages: list) -> Tuple[str, str]:
    """Calls the LLM and parses the response."""
    if not client:
        return "⚠️ Configure your Groq API Key in the sidebar.", ""

    history = [{"role": m["role"], "content": m["content"]} for m in messages[-12:]]
    history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": build_system_prompt(profile, progress, LANGUAGES, LEVELS)},
                *history,
            ],
            temperature=0.7,
            max_tokens=600,
        )
        full = response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return f"Error calling Groq: {e}", ""

    # Parse note
    note = ""
    main = full
    if "[[" in full and "]]" in full:
        start = full.index("[[")
        end = full.index("]]") + 2
        note = full[start+2:end-2].strip()
        main = (full[:start] + full[end:]).strip()
        if note.lower().startswith("note:"):
            note = note[5:].strip()

    return main, note

def transcribe_audio(client: Groq, audio_bytes: bytes, language: str) -> str:
    """Transcribes audio using Groq Whisper."""
    if not client:
        return ""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            f.flush()
            with open(f.name, "rb") as audio_file:
                lang_code = LANGUAGES.get(language, {}).get("code", "fr")
                result = client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file,
                    language=lang_code,
                )
        return result.text.strip()
    except Exception as e:
        logging.error(f"Audio transcription failed: {e}")
        return ""

async def _tts_async(text: str, voice: str) -> bytes:
    """Async TTS using edge-tts."""
    communicate = edge_tts.Communicate(text, voice)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

def autoplay_audio(audio_bytes: bytes):
    """Plays audio in Streamlit."""
    b64 = base64.b64encode(audio_bytes).decode()
    st.markdown(
        f'<audio autoplay style="display:none"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
        unsafe_allow_html=True,
    )

def compute_progress_pct(turns: int, level: str) -> float:
    """Computes progress percentage."""
    target = LEVEL_TURNS.get(level, 20)
    return min(turns / target, 1.0)

def update_progress(progress: dict, note: str):
    """Updates session progress."""
    progress["turns"] += 1
    progress["score"] += 10
    if note and any(w in note.lower() for w in ["error", "incorrect", "mistake"]):
        progress["score"] = max(0, progress["score"] - 3)
        progress["errors"].append(f"Turn {progress['turns']}")

def synthesize_speech(text: str) -> bytes | None:
    """TTS en el idioma que se aprende."""
    voice = LANGUAGES.get(
        st.session_state.profile["language"], {}
    ).get("voice", "fr-FR-DeniseNeural")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio = loop.run_until_complete(_tts_async(text, voice))
        loop.close()
        return audio
    except Exception as e:
        st.error(f"Error TTS: {e}")
        return None

def synthesize_speech_native(text: str) -> bytes | None:
    """TTS en el idioma nativo del alumno (para correcciones)."""
    NATIVE_VOICES = {
        "Español":   "es-ES-ElviraNeural",
        "Inglés":    "en-US-AriaNeural",
        "Francés":   "fr-FR-DeniseNeural",
        "Portugués": "pt-BR-FranciscaNeural",
        "Alemán":    "de-DE-KatjaNeural",
    }
    voice = NATIVE_VOICES.get(
        st.session_state.profile.get("native", "Español"),
        "es-ES-ElviraNeural"
    )
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio = loop.run_until_complete(_tts_async(text, voice))
        loop.close()
        return audio
    except Exception as e:
        st.error(f"Error TTS nativo: {e}")
        return None


HTML_CODE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:        #0e0e0f;
    --surface:   #161618;
    --border:    #2a2a2e;
    --accent:    #c8f060;
    --accent2:   #60c8f0;
    --muted:     #5a5a66;
    --text:      #e8e8ec;
    --text-dim:  #9090a0;
    --user-bg:   #1a1f1a;
    --bot-bg:    #111318;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem; max-width: 100%; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Playfair Display', serif;
    color: var(--accent);
}

/* ── App title ── */
.app-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.app-title span { color: var(--accent); }
.app-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── Chat messages ── */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.msg-user {
    background: var(--user-bg);
    border: 1px solid #2a3a2a;
    border-radius: 16px 16px 4px 16px;
    padding: 1rem 1.2rem;
    align-self: flex-end;
    max-width: 75%;
}
.msg-bot {
    background: var(--bot-bg);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px;
    padding: 1rem 1.2rem;
    align-self: flex-start;
    max-width: 80%;
}

.msg-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}
.msg-user .msg-label { color: var(--accent); }
.msg-bot .msg-label  { color: var(--accent2); }

.msg-text {
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text);
}

.msg-note {
    margin-top: 0.6rem;
    padding-top: 0.6rem;
    border-top: 1px solid var(--border);
    font-size: 0.8rem;
    color: var(--text-dim);
    font-style: italic;
}

.msg-correction {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    background: linear-gradient(135deg, #1c1a10 0%, #2a2010 100%);
    border: 1px solid #f0a06044;
    border-left: 3px solid #f0a060;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.75rem;
}
.correction-icon {
    font-size: 1.1rem;
    flex-shrink: 0;
    margin-top: 0.1rem;
}
.correction-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: #f0a060;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.correction-text {
    font-size: 0.88rem;
    color: #f0d0a0;
    line-height: 1.5;
}
.msg-note {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border);
    font-size: 0.82rem;
    color: var(--text-dim);
    font-style: italic;
    line-height: 1.5;
}
.note-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    color: var(--accent2);
    text-transform: uppercase;
    font-style: normal;
    margin-bottom: 0.25rem;
}

/* ── Progress bar ── */
.progress-wrap {
    background: var(--border);
    border-radius: 4px;
    height: 6px;
    margin: 0.4rem 0 1rem 0;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 4px;
    transition: width 0.6s ease;
}

/* ── Stat pills ── */
.stat-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}
.stat-pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-dim);
}
.stat-pill b { color: var(--accent); }

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0e0e0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1.2rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Secondary button */
.stButton.secondary > button {
    background: transparent !important;
    color: var(--text-dim) !important;
    border: 1px solid var(--border) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1rem 0; }

/* ── Section headers ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* ── Recording indicator ── */
.rec-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #f06060;
}
.rec-dot {
    width: 8px; height: 8px;
    background: #f06060;
    border-radius: 50%;
    animation: pulse 1s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* Expander */
[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border) !important;
    border-radius: 10px;
}
</style>
"""