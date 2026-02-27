import asyncio
import hashlib
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import DEFAULT_PROFILE, DEFAULT_PROGRESS, LANGUAGES, LEVELS, LEVEL_TURNS, NATIVE_VOICES
from prompts.prompts import build_system_prompt, get_intro_message
from utils import call_llm, get_client, synthesize_speech, synthesize_speech_native, transcribe_audio

load_dotenv()
_SERVER_API_KEY = os.getenv("GROQ_API_KEY", "")

app = FastAPI(title="LangTeach API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    profile: dict
    progress: dict
    messages: list
    api_key: str

class InitRequest(BaseModel):
    profile: dict
    api_key: str

class TTSRequest(BaseModel):
    text: str
    language: str
    native: str
    speak_correction: bool = True
    correction_text: str = ""

class TranscribeRequest(BaseModel):
    audio_b64: str
    language: str
    api_key: str

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def parse_response(response: str):
    """Extract correction from <<<...>>> and note from [[...]]."""
    correction = ""
    note = ""
    main = response

    if "<<<" in main and ">>>" in main:
        cs = main.index("<<<")
        ce = main.index(">>>") + 3
        correction = main[cs + 3:ce - 3].strip()
        main = (main[:cs] + main[ce:]).strip()

    if "[[" in main and "]]" in main:
        ns = main.index("[[")
        ne = main.index("]]") + 2
        note = main[ns + 2:ne - 2].strip()
        if note.lower().startswith("note:"):
            note = note[5:].strip()
        main = (main[:ns] + main[ne:]).strip()

    return main.strip(), correction.strip(), note.strip()


def compute_progress(progress: dict, level: str) -> float:
    target = LEVEL_TURNS.get(level, 20)
    return min(progress.get("turns", 0) / target, 1.0)

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/api/config")
async def get_config():
    return {
        "languages": {k: {"code": v["code"], "flag": v["flag"]} for k, v in LANGUAGES.items()},
        "levels": LEVELS,
        "defaults": DEFAULT_PROFILE,
        "server_has_key": bool(_SERVER_API_KEY),  # indica al frontend si hay key en servidor
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    api_key = req.api_key or _SERVER_API_KEY
    client = get_client(api_key)
    if not client:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    raw, note = call_llm(client, req.message, req.profile, req.progress, req.messages)
    main, correction, note = parse_response(raw) if "<<<" not in raw else (
        *parse_response(raw)[:2], note
    )
    # Re-parse properly
    main, correction, note_parsed = parse_response(raw)
    if not note_parsed and note:
        note_parsed = note

    return {
        "main":       main,
        "correction": correction,
        "note":       note_parsed,
        "timestamp":  datetime.now().strftime("%H:%M"),
    }


@app.post("/api/init")
async def init_session(req: InitRequest):
    """Fire the intro message to get the tutor's opening turn."""
    api_key = req.api_key or _SERVER_API_KEY
    client = get_client(api_key)
    if not client:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    intro = get_intro_message(req.profile)
    raw, note = call_llm(client, intro, req.profile, {**DEFAULT_PROGRESS}, [])
    main, correction, note_parsed = parse_response(raw)
    if not note_parsed and note:
        note_parsed = note

    return {
        "intro_user":  intro,
        "main":        main,
        "correction":  correction,
        "note":        note_parsed,
        "timestamp":   datetime.now().strftime("%H:%M"),
    }


@app.post("/api/tts")
async def tts(req: TTSRequest):
    """Returns combined audio: correction (native) + main response (target language)."""
    import base64
    from utils import _tts_async

    audio_parts = []

    if req.speak_correction and req.correction_text:
        voice = NATIVE_VOICES.get(req.native, "en-US-AriaNeural")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_c = loop.run_until_complete(_tts_async(req.correction_text, voice))
            loop.close()
            if audio_c:
                audio_parts.append(audio_c)
        except Exception:
            pass

    if req.text:
        voice = LANGUAGES.get(req.language, {}).get("voice", "en-US-AriaNeural")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_r = loop.run_until_complete(_tts_async(req.text, voice))
            loop.close()
            if audio_r:
                audio_parts.append(audio_r)
        except Exception:
            pass

    if not audio_parts:
        raise HTTPException(status_code=500, detail="TTS failed")

    combined = b"".join(audio_parts)
    b64 = base64.b64encode(combined).decode()
    return {"audio_b64": b64}


@app.post("/api/transcribe")
async def transcribe(req: TranscribeRequest):
    """Transcribes base64-encoded audio."""
    import base64
    from utils import transcribe_audio

    api_key = req.api_key or _SERVER_API_KEY
    client = get_client(api_key)
    if not client:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    audio_bytes = base64.b64decode(req.audio_b64)
    text = transcribe_audio(client, audio_bytes, req.language)
    return {"text": text}


# Mount static files last
app.mount("/static", StaticFiles(directory="static"), name="static")