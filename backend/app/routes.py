from fastapi import APIRouter, HTTPException
from db import engine
from models import Hotspot
from chat_utils import build_prompt, call_openai, simple_response
from redaction import redact
import json
router = APIRouter()
@router.get('/hotspots')
def hotspots(date: str):
    q = 'SELECT * FROM daily_hotspots WHERE agg_date = :d'
    with engine.connect() as conn:
        res = conn.execute(q, {'d': date}).mappings().all()
    return [dict(r) for r in res]
@router.post('/chat')
def chat(body: dict):
    text = body.get('message','')
    district = body.get('district')
    redacted = redact(text)
    # simple danger detection + resources
    reply, escalation = simple_response(redacted)
    if 'OPENAI_API_KEY' in __import__('os').environ:
        prompt = build_prompt(redacted, [])
        model_reply = call_openai(prompt)
        if model_reply:
            reply = model_reply
    resources = []
    try:
        with open('../data/resources.json') as f:
            allr = json.load(f)
            for r in allr:
                if district and (r.get('district')==district or r.get('district')=='National'):
                    resources.append(r)
            if not resources:
                resources = [r for r in allr if r.get('district')=='National']
    except Exception:
        resources = []
    return {'reply': reply, 'resources': resources, 'escalation_flag': escalation}
