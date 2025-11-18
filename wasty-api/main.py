# service_b.py
import os, json
from typing import Optional
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
QDRANT_URL     = os.environ.get("QDRANT_URL", "http://localhost:6333")
COLLECTION     = os.environ.get("QDRANT_COLLECTION", "wasty_docs")
EMBED_MODEL    = os.environ.get("EMBED_MODEL", "text-embedding-3-small")
TOP_K          = int(os.environ.get("TOP_K", "5"))
MIN_SCORE      = float(os.environ.get("MIN_SCORE", "0.4"))

BLOCK_WORDS = {"password", "admin access", "bypass", "prompt injection"}

app = FastAPI(title="wasty-api", version="1.0")

class AnalyzeRequest(BaseModel):
    item: str

def embed_text(client: OpenAI, text: str):
    r = client.embeddings.create(model=EMBED_MODEL, input=[text])
    return r.data[0].embedding

def qdrant_search(vec):
    body = {"vector": vec, "limit": TOP_K, "with_payload": True}
    r = requests.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
                      headers={"Content-Type":"application/json"},
                      data=json.dumps(body))
    if r.status_code >= 400:
        raise HTTPException(502, f"Qdrant-Fehler: {r.status_code} {r.text}")
    return r.json().get("result", [])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    if any(w in req.item.lower() for w in BLOCK_WORDS):
        return {"alert": "blocked", "reason": "Sicherheits-Schlüsselwort erkannt"}
    client = OpenAI(api_key=OPENAI_API_KEY)
    vec = embed_text(client, req.item)
    hits = qdrant_search(vec)
    if not hits or hits[0]["score"] < MIN_SCORE:
        return {"alert": "unknown", "reason": "Keine ausreichende Ähnlichkeit"}
    return {"alert": "similar-pattern", "category": hits[0]["payload"].get("category")}
