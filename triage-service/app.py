from fastapi import FastAPI
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

@app.get("/")
async def root():
    return {
        "service": "H.E.L.P-Q Triage Service",
        "status": "Operational",
        "port": 8001,
        "docs": "http://127.0.0.1:8001/docs",
        "endpoint": "POST /triage"
    }


@app.post("/triage")
async def triage(text: str):
    doc = nlp(text.lower())
    # Extract nouns and adjectives
    extracted = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    
    critical = ["chest pain", "breathless", "unconscious", "heart"]
    is_emergency = any(c in text.lower() for c in critical)
    
    # Return a structured dictionary
    return {"symptoms": extracted, "emergency": is_emergency}