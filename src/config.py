LANGUAGES = {
    "Francés":    {"code": "fr", "voice": "fr-FR-DeniseNeural",    "flag": "🇫🇷"},
    "Inglés":     {"code": "en", "voice": "en-US-AriaNeural",       "flag": "🇺🇸"},
    "Alemán":     {"code": "de", "voice": "de-DE-KatjaNeural",      "flag": "🇩🇪"},
    "Italiano":   {"code": "it", "voice": "it-IT-ElsaNeural",       "flag": "🇮🇹"},
    "Portugués":  {"code": "pt", "voice": "pt-BR-FranciscaNeural",  "flag": "🇧🇷"},
    "Japonés":    {"code": "ja", "voice": "ja-JP-NanamiNeural",     "flag": "🇯🇵"},
    "Chino":      {"code": "zh", "voice": "zh-CN-XiaoxiaoNeural",   "flag": "🇨🇳"},
    "Árabe":      {"code": "ar", "voice": "ar-EG-SalmaNeural",      "flag": "🇸🇦"},
    "Ruso":       {"code": "ru", "voice": "ru-RU-SvetlanaNeural",   "flag": "🇷🇺"},
    "Coreano":    {"code": "ko", "voice": "ko-KR-SunHiNeural",      "flag": "🇰🇷"},
}

LEVELS = {
    "A1": "Absolute beginner — very simple phrases, basic vocabulary",
    "A2": "Elementary — can communicate in simple and routine tasks",
    "B1": "Intermediate — can handle familiar situations",
    "B2": "Upper-intermediate — can speak fluently on varied topics",
    "C1": "Advanced — can express ideas spontaneously and precisely",
    "C2": "Proficient — near-native mastery of the language",
}

LEVEL_TURNS = {"A1": 10, "A2": 15, "B1": 20, "B2": 25, "C1": 30, "C2": 40}

# Otras constantes
DEFAULT_PROFILE = {
    "language": "Italiano",
    "level": "A2",
    "topic": "Daily conversation",
    "native": "Español",
}

DEFAULT_PROGRESS = {
    "turns": 0,
    "errors": [],
    "vocab_seen": [],
    "score": 0,
}