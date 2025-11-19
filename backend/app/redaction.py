
import re
def redact(text: str):
    # remove emails
    red = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '[REDACTED_EMAIL]', text)
    # remove SA ID numbers (13 digits)
    red = re.sub(r'\b\d{13}\b', '[REDACTED_ID]', red)
    # remove phone numbers (simple)
    red = re.sub(r'(\+?\d[\d\-\s]{7,}\d)', '[REDACTED_PHONE]', red)
    # remove sequences of Capitalized Words that look like names (heuristic)
    red = re.sub(r'\\b([A-Z][a-z]{1,}\\s[A-Z][a-z]{1,})\\b', '[REDACTED_NAME]', red)
    return red
