import streamlit as st
import os
import json
import hashlib
from datetime import datetime
from dotenv import load_dotenv

from utils import *
load_dotenv()

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LangTeach · Tutor de Idiomas",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(HTML_CODE, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "messages":        [],
        "profile":         DEFAULT_PROFILE,
        "progress":        {**DEFAULT_PROGRESS},
        "session_start":   datetime.now().isoformat(),
        "api_key":         os.getenv("GROQ_API_KEY", ""),
        "setup_done":      False,
        "last_audio_hash": None,
        "pending_audio":   None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# PROGRESS HELPERS
# ─────────────────────────────────────────────
def compute_progress_pct() -> float:
    turns  = st.session_state.progress["turns"]
    target = LEVEL_TURNS.get(st.session_state.profile["level"], 20)
    return min(turns / target, 1.0)

def update_progress(note: str):
    st.session_state.progress["turns"] += 1
    st.session_state.progress["score"] += 10
    if note and any(w in note.lower() for w in ["error", "incorrecto", "equivoc", "incorrect", "mistake"]):
        st.session_state.progress["score"] = max(0, st.session_state.progress["score"] - 3)
        st.session_state.progress["errors"].append(f"Turno {st.session_state.progress['turns']}")

# ─────────────────────────────────────────────
# RENDER CHAT
# ─────────────────────────────────────────────
def render_chat():
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding: 3rem 0; color: #5a5a66;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">🗣️</div>
            <div style="font-family:'DM Mono',monospace; font-size:0.8rem; letter-spacing:0.1em;">
                EMPIEZA A HABLAR O ESCRIBE ABAJO
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    html = '<div class="chat-wrapper">'
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            html += f"""
            <div class="msg-user">
                <div class="msg-label">Tú · {msg.get("timestamp","")}</div>
                <div class="msg-text">{msg["content"]}</div>
            </div>"""
        else:
            correction_html = ""
            if msg.get("correction"):
                correction_html = f"""
                <div class="msg-correction">
                    <span class="correction-icon">🎯</span>
                    <div class="correction-body">
                        <div class="correction-label">CORRECCIÓN / CONSEJO</div>
                        <div class="correction-text">{msg["correction"]}</div>
                    </div>
                </div>"""
            note_html = ""
            if msg.get("note"):
                note_html = f"""
                <div class="msg-note">
                    <span>💡</span>
                    <div>
                        <div class="note-label">NOTA PEDAGÓGICA</div>
                        <div>{msg["note"]}</div>
                    </div>
                </div>"""
            html += f"""
            <div class="msg-bot">
                <div class="msg-label">LangTeach · {msg.get("timestamp","")}</div>
                {correction_html}
                <div class="msg-text">{msg["content"]}</div>
                {note_html}
            </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SEND MESSAGE FLOW
# ─────────────────────────────────────────────
def send_message(user_text: str):
    if not user_text.strip():
        return

    client = get_client(st.session_state.api_key)
    ts = datetime.now().strftime("%H:%M")

    st.session_state.messages.append({
        "role": "user", "content": user_text, "note": "", "timestamp": ts,
    })

    with st.spinner("LangTeach está pensando..."):
        response, note = call_llm(
            client, user_text,
            st.session_state.profile,
            st.session_state.progress,
            st.session_state.messages[:-1],  # excluir el mensaje recién añadido
        )

    # Parsear corrección <<<...>>> de la respuesta principal
    correction = ""
    main = response
    if "<<<" in response and ">>>" in response:
        cs = response.index("<<<")
        ce = response.index(">>>") + 3
        correction = response[cs+3:ce-3].strip()
        main = (response[:cs] + response[ce:]).strip()

    update_progress(note)

    st.session_state.messages.append({
        "role":       "assistant",
        "content":    main,
        "note":       note,
        "correction": correction,
        "timestamp":  datetime.now().strftime("%H:%M"),
    })

    # TTS
    audio_parts = []
    if correction:
        audio_c = synthesize_speech_native(correction)
        if audio_c:
            audio_parts.append(audio_c)
    if main and not main.startswith("⚠️"):
        audio_r = synthesize_speech(main)
        if audio_r:
            audio_parts.append(audio_r)
    if audio_parts:
        st.session_state["pending_audio"] = b"".join(audio_parts)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1.5rem 0;">
        <div style="font-family:'Playfair Display',serif; font-size:1.6rem; font-weight:700; color:#c8f060;">LangTeach</div>
        <div style="font-family:'DM Mono',monospace; font-size:0.65rem; color:#5a5a66; letter-spacing:0.1em; text-transform:uppercase;">Tutor conversacional</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">🔑 API Key (Groq)</div>', unsafe_allow_html=True)
    api_input = st.text_input("Groq API Key", value=st.session_state.api_key,
                               type="password", label_visibility="collapsed", placeholder="gsk_...")
    if api_input != st.session_state.api_key:
        st.session_state.api_key = api_input

    st.markdown("---")
    st.markdown('<div class="section-label">⚙️ Configuración</div>', unsafe_allow_html=True)

    lang = st.selectbox("Idioma a aprender", list(LANGUAGES.keys()),
                         index=list(LANGUAGES.keys()).index(st.session_state.profile["language"]))
    level = st.selectbox("Tu nivel actual", list(LEVELS.keys()),
                          index=list(LEVELS.keys()).index(st.session_state.profile["level"]))
    topic = st.text_input("Tema de práctica", value=st.session_state.profile["topic"],
                           placeholder="Ej: pedir comida en un restaurante")
    native = st.selectbox("Tu idioma nativo", ["Español", "Inglés", "Francés", "Portugués", "Alemán"], index=0)

    if st.button("Aplicar configuración"):
        st.session_state.profile  = {"language": lang, "level": level, "topic": topic, "native": native}
        st.session_state.messages = []
        st.session_state.progress = {**DEFAULT_PROGRESS}
        st.session_state.setup_done = False
        st.success("¡Nueva sesión iniciada!")
        st.rerun()

    st.markdown("---")
    st.markdown('<div class="section-label">📊 Progreso de sesión</div>', unsafe_allow_html=True)
    prog = st.session_state.progress
    pct  = compute_progress_pct()
    flag = LANGUAGES.get(st.session_state.profile["language"], {}).get("flag", "")

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-pill">{flag} {st.session_state.profile["language"]}</div>
        <div class="stat-pill">Nivel <b>{st.session_state.profile["level"]}</b></div>
        <div class="stat-pill"><b>{prog["turns"]}</b> turnos</div>
        <div class="stat-pill"><b>{prog["score"]}</b> pts</div>
    </div>
    <div class="progress-wrap"><div class="progress-fill" style="width:{int(pct*100)}%"></div></div>
    <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#5a5a66;text-align:right;">{int(pct*100)}% de la sesión objetivo</div>
    """, unsafe_allow_html=True)

    if prog["errors"]:
        with st.expander(f"⚠️ Errores ({len(prog['errors'])})"):
            for e in prog["errors"]:
                st.markdown(f"- {e}")

    st.markdown("---")
    if st.button("🔄 Nueva sesión"):
        st.session_state.messages  = []
        st.session_state.progress  = {**DEFAULT_PROGRESS}
        st.session_state.setup_done = False
        st.rerun()

    if st.session_state.messages:
        chat_export = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
        st.download_button("💾 Exportar conversación", data=chat_export,
                            file_name=f"langteach_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                            mime="application/json")

# ─────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────
flag = LANGUAGES.get(st.session_state.profile["language"], {}).get("flag", "")
st.markdown(f"""
<div class="app-title">Lang<span>Teach</span></div>
<div class="app-subtitle">{flag} Tutor de {st.session_state.profile["language"]} · Nivel {st.session_state.profile["level"]} · {st.session_state.profile["topic"]}</div>
""", unsafe_allow_html=True)

# Audio pendiente
if st.session_state.get("pending_audio"):
    autoplay_audio(st.session_state["pending_audio"])
    st.session_state["pending_audio"] = None

with st.container():
    render_chat()

st.markdown("---")

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("Escribe aquí", key="text_input",
                                placeholder=f"Escribe en {st.session_state.profile['language']}... o usa el micrófono →",
                                label_visibility="collapsed")
with col2:
    send_btn = st.button("Enviar →", use_container_width=True)

st.markdown('<div class="section-label" style="margin-top:0.8rem;">🎙️ Entrada de voz</div>', unsafe_allow_html=True)

try:
    from audio_recorder_streamlit import audio_recorder
    audio_bytes = audio_recorder(text="Pulsa para grabar", recording_color="#c8f060",
                                  neutral_color="#5a5a66", icon_name="microphone",
                                  icon_size="2x", pause_threshold=2.5, sample_rate=16000)
    if audio_bytes and len(audio_bytes) > 10000:
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        if audio_hash != st.session_state.last_audio_hash:
            st.session_state.last_audio_hash = audio_hash
            with st.spinner("Transcribiendo..."):
                client = get_client(st.session_state.api_key)
                transcribed = transcribe_audio(client, audio_bytes, st.session_state.profile["language"])
            if transcribed:
                send_message(transcribed)
                st.rerun()
except ImportError:
    st.info("Instala `audio-recorder-streamlit` para usar el micrófono.")

if send_btn and user_input:
    send_message(user_input)
    st.rerun()

# Auto-start
if not st.session_state.setup_done and st.session_state.api_key and not st.session_state.messages:
    st.session_state.setup_done = True
    client = get_client(st.session_state.api_key)
    with st.spinner("Iniciando sesión..."):
        intro = get_intro_message(st.session_state.profile)
        response, note = call_llm(client, intro, st.session_state.profile,
                                   st.session_state.progress, [])
        # Parsear corrección del mensaje inicial
        correction = ""
        main = response
        if "<<<" in response and ">>>" in response:
            cs = response.index("<<<")
            ce = response.index(">>>") + 3
            correction = response[cs+3:ce-3].strip()
            main = (response[:cs] + response[ce:]).strip()

        update_progress(note)
        ts = datetime.now().strftime("%H:%M")
        st.session_state.messages.append(
            {"role": "user", "content": intro, "note": "", "timestamp": ts})
        st.session_state.messages.append({
            "role": "assistant", "content": main, "note": note,
            "correction": correction, "timestamp": datetime.now().strftime("%H:%M"),
        })
        if main and not main.startswith("⚠️"):
            audio = synthesize_speech(main)
            if audio:
                st.session_state["pending_audio"] = audio
    st.rerun()

elif not st.session_state.api_key:
    st.markdown("""
    <div style="background:#1a1010;border:1px solid #3a2020;border-radius:10px;
                padding:1rem 1.2rem;margin-top:1rem;font-size:0.9rem;color:#f0a0a0;">
        ⚠️ Añade tu <b>API Key de Groq</b> en la barra lateral para comenzar.
        Consíguela gratis en <a href="https://console.groq.com" target="_blank" style="color:#c8f060;">console.groq.com</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:2rem;font-family:'DM Mono',monospace;
            font-size:0.65rem;color:#3a3a44;letter-spacing:0.1em;">
    LangTeach · GROQ LLAMA 3.3 · WHISPER · EDGE-TTS · STREAMLIT
</div>
""", unsafe_allow_html=True)