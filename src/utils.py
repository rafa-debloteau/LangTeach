import asyncio
import base64
import logging
import tempfile
from typing import Optional, Tuple

import edge_tts
from groq import Groq

from config import LANGUAGES, LEVELS, NATIVE_VOICES
from prompts import build_system_prompt

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
        return "⚠️ Configure your Groq API Key.", ""

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

    # Parse pedagogical note [[...]]
    note = ""
    main = full
    if "[[" in full and "]]" in full:
        start = full.index("[[")
        end   = full.index("]]") + 2
        note  = full[start + 2:end - 2].strip()
        main  = (full[:start] + full[end:]).strip()
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
                lang_code = LANGUAGES.get(language, {}).get("code", "en")
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


def synthesize_speech(text: str, language: str) -> bytes | None:
    """TTS in the target language."""
    voice = LANGUAGES.get(language, {}).get("voice", "en-US-AriaNeural")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio = loop.run_until_complete(_tts_async(text, voice))
        loop.close()
        return audio
    except Exception as e:
        logging.error(f"TTS error: {e}")
        return None


def synthesize_speech_native(text: str, native: str) -> bytes | None:
    """TTS in the student's native language (for corrections)."""
    voice = NATIVE_VOICES.get(native, "en-US-AriaNeural")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio = loop.run_until_complete(_tts_async(text, voice))
        loop.close()
        return audio
    except Exception as e:
        logging.error(f"Native TTS error: {e}")
        return None