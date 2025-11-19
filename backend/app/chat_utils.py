import os, openai, time
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SYSTEM_PROMPT = """You are a compassionate assistant specialized in non-judgmental support
for gender-based-violence survivors and advocates in South Africa. Do NOT ask for identifiers.
If user indicates imminent danger, recommend calling emergency services and provide hotlines.
Provide resource suggestions and short safe scripts for contacting authorities or advocates.
"""
def build_prompt(user_text, resources=[]):
    prompt = SYSTEM_PROMPT + "\n\nUser: " + user_text + "\n\nRespond concisely, empathetically, and include resource suggestions if available."
    return prompt
def call_openai(prompt):
    if not OPENAI_API_KEY:
        raise RuntimeError('No OPENAI_API_KEY configured')
    openai.api_key = OPENAI_API_KEY
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini' if 'gpt-4o-mini' in openai.Model.list() else 'gpt-4o',
            messages=[{'role':'system','content':SYSTEM_PROMPT},{'role':'user','content':prompt}],
            max_tokens=300
        )
        return resp['choices'][0]['message']['content']
    except Exception as e:
        return None
def simple_response(text):
    # fallback deterministic responses
    txt = text.lower()
    if any(k in txt for k in ['help me now','being assaulted','right now','now']):
        return "I'm sorry — if you are in immediate danger please call your local emergency number or the GBV Command Centre at 0800 428 428.", True
    if 'hotline' in txt or 'help' in txt:
        return "You can call the GBV Command Centre at 0800 428 428. If you tell me your district I can look up local shelters.", False
    return "I hear you. Can you tell me which district or city you're in? I can suggest local resources and steps to stay safe.", False
