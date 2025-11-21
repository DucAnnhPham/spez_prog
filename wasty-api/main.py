# service_b.py
import os, json
from typing import Optional
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from sentence_transformers import SentenceTransformer

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
QDRANT_URL     = os.environ.get("QDRANT_URL", "http://localhost:6333")
COLLECTION     = os.environ.get("QDRANT_COLLECTION", "wasty_docs")
EMBED_MODEL    = os.environ.get("EMBED_MODEL", "text-embedding-3-small")
LOCAL_MODEL    = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
TOP_K          = int(os.environ.get("TOP_K", "5"))
MIN_SCORE      = float(os.environ.get("MIN_SCORE", "0.6"))

BLOCK_WORDS = {"password", "admin access", "bypass", "prompt injection"}

app = FastAPI(title="wasty-api", version="1.0")

class AnalyzeRequest(BaseModel):
    item: str

def get_min_score():
    if OPENAI_API_KEY:      # bei Openai kann der score etwas niedriger sein, weil ein zu hoher Wert oft zu keinen Treffern führt
        return 0.5          # text-embedding-3-small hat eine Dimension von 1536
    else:                   # bei lokalen Embeddings lieber etwas strenger sein
        return 0.65         # all-MiniLM-L6-v2 hat hingegen nur eine Dimension von 384 deswefen sollten wir strenger sein



def embed_texts(client: Optional[OpenAI], texts):
    if client is not None and OPENAI_API_KEY:
        resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
        return [d.embedding for d in resp.data]
    else:
        # lokale Embeddings mit SentenceTransformer
        return LOCAL_MODEL.encode(texts, show_progress_bar=False).tolist()


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
    client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
    vec = embed_texts(client, [req.item])[0]
    hits = qdrant_search(vec)
    if not hits or hits[0]["score"] < get_min_score():
        return {"alert": "unknown Object", "reason": "Keine ausreichende Ähnlichkeit"}
    return {"alert": "similar-pattern", "category": hits[0]["payload"].get("category")}
