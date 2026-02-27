from prompts.italian import ITALIAN_CONFIG, ITALIAN_SYSTEM_PROMPT_EXTRA
from prompts.english import ENGLISH_CONFIG, ENGLISH_SYSTEM_PROMPT_EXTRA
from prompts.french import FRENCH_CONFIG, FRENCH_SYSTEM_PROMPT_EXTRA

LANGUAGE_REGISTRY = {
    "Italian":  {"config": ITALIAN_CONFIG,  "extra_prompt": ITALIAN_SYSTEM_PROMPT_EXTRA},
    "French":   {"config": FRENCH_CONFIG,   "extra_prompt": FRENCH_SYSTEM_PROMPT_EXTRA},
    "English":  {"config": ENGLISH_CONFIG,  "extra_prompt": ENGLISH_SYSTEM_PROMPT_EXTRA},
}

def get_language_config(language_name: str) -> dict:
    """Returns config for the requested language, or a generic fallback."""
    return LANGUAGE_REGISTRY.get(language_name, {}).get("config", {})

def get_language_extra_prompt(language_name: str) -> str:
    """Returns language-specific extra prompt instructions."""
    return LANGUAGE_REGISTRY.get(language_name, {}).get("extra_prompt", "")

def get_curriculum(language_name: str, level: str) -> dict:
    """Returns the curriculum for a given language and level."""
    config = get_language_config(language_name)
    return config.get("curriculum", {}).get(level, {})

def get_all_languages() -> list[str]:
    """Returns all registered language names."""
    return list(LANGUAGE_REGISTRY.keys())



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

NATIVE_VOICES = {
    "Spanish":    "es-ES-ElviraNeural",
    "English":    "en-US-AriaNeural",
    "French":     "fr-FR-DeniseNeural",
    "Portuguese": "pt-BR-FranciscaNeural",
    "German":     "de-DE-KatjaNeural",
}

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