import logging
import sys
from langdetect import detect

# 1. Standard Logger Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("2CareVoiceAgent")

# 2. Language Detection Helper
def identify_language(text: str):
    try:
        lang = detect(text)
        # mapping ISO codes to names
        mapping = {"en": "English", "hi": "Hindi", "ta": "Tamil"}
        return mapping.get(lang, "English")
    except Exception:
        return "Unknown"