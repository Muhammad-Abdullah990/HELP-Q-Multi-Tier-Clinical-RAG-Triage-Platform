from shared.utils import log

EMERGENCY_KEYWORDS = [
    "chest pain",
    "breathing difficulty",
    "unconscious",
    "severe bleeding"
]

def check_emergency(text):
    log("Checking emergency...")

    for word in EMERGENCY_KEYWORDS:
        if word in text.lower():
            return True
    return False