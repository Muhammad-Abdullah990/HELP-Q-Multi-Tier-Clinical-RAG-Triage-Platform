from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
import os
import sys
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.rag_engine import synthesize_rag_response

app = FastAPI(title="H.E.L.P-Q RAG Gateway")

# Enable CORS for Frontend UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Session Memory
chat_memory = []

def contains_word(text: str, keywords: list) -> bool:
    for kw in keywords:
        # Match whole word boundaries (e.g. 'how' matches 'how' but NOT 'shower')
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

@app.get("/")
async def root():
    return {
        "service": "H.E.L.P-Q Chat Gateway & RAG Engine",
        "status": "Operational",
        "port": 8000,
        "docs": "http://127.0.0.1:8000/docs",
        "endpoint": "POST /chat"
    }


@app.post("/chat")
async def chat(user_query: str):
    global chat_memory
    q_lower = user_query.lower()

    # --- LAYER 1: THE FIREWALL (Emergency & Support with Exact Word Boundaries) ---
    emergency_keywords = ["chest pain", "breath", "unconscious", "bleeding"]
    if contains_word(q_lower, emergency_keywords):
        return {
            "reply": "EMERGENCY: Please seek immediate medical attention or call 1122/911.",
            "recommended_doctor": "Emergency Room (ER)",
            "architecture_trace": {
                "Layer_1_Gateway_Firewall": {"port": 8000, "status": "TRIGGERED", "reason": "Emergency keyword detected", "action": "Immediate ER Escalation"},
                "Layer_2_Triage_Service": {"port": 8001, "status": "BYPASSED", "reason": "Emergency Protocol Safety Bypass"},
                "Layer_3_Diagnosis_Service": {"port": 8002, "status": "BYPASSED", "reason": "Emergency Protocol Safety Bypass"},
                "Layer_4_Recommendation_Service": {"port": 8003, "status": "BYPASSED", "reason": "Emergency Protocol Safety Bypass"},
                "Layer_5_RAG_Synthesizer": {"status": "BYPASSED", "reason": "Emergency Protocol Safety Bypass"}
            },
            "details": {"description": "Life-threatening symptoms detected.", "precautions": ["Keep calm", "Don't drive"]}
        }

    support_keywords = ["how does", "system work", "who built", "what model"]
    if contains_word(q_lower, support_keywords):
        return {
            "reply": "I am the H.E.L.P-Q Engine. I process symptoms through a spaCy NLP triage, Random Forest ML model, and Gemini RAG synthesizer to route you to the correct specialist.",
            "recommended_doctor": "System Support",
            "architecture_trace": {
                "Layer_1_Gateway_Firewall": {"port": 8000, "status": "SUPPORT_MODE", "action": "System Information"},
                "Layer_2_Triage_Service": {"port": 8001, "status": "NOT_NEEDED"},
                "Layer_3_Diagnosis_Service": {"port": 8002, "status": "NOT_NEEDED"},
                "Layer_4_Recommendation_Service": {"port": 8003, "status": "NOT_NEEDED"},
                "Layer_5_RAG_Synthesizer": {"status": "NOT_NEEDED"}
            },
            "details": {"status": "Operational"}
        }

    # --- LAYER 2, 3, 4, 5: TRIAGE, DIAGNOSIS, RECOMMENDATION & GEMINI RAG SYNTHESIS ---
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Step 1: Triage (Layer 2)
            t_res = await client.post("http://localhost:8001/triage", params={"text": user_query})
            triage_data = t_res.json()
            symptoms = triage_data.get('symptoms', [])

            if len(symptoms) == 0:
                return {
                    "reply": "I couldn't identify specific medical symptoms in your query. Could you describe your physical discomfort or pain more clearly?",
                    "recommended_doctor": "General Physician (Consultation)",
                    "architecture_trace": {
                        "Layer_1_Gateway_Firewall": {"port": 8000, "status": "PASSED", "result": "Safe"},
                        "Layer_2_Triage_Service": {"port": 8001, "status": "NO_SYMPTOMS_FOUND", "extracted": []},
                        "Layer_3_Diagnosis_Service": {"port": 8002, "status": "SKIPPED"},
                        "Layer_4_Recommendation_Service": {"port": 8003, "status": "FALLBACK"},
                        "Layer_5_RAG_Synthesizer": {"status": "FALLBACK"}
                    }
                }

            # Step 2: Diagnosis (Layer 3)
            d_res = await client.post("http://localhost:8002/diagnose", json={"symptoms": symptoms})
            diagnosis_data = d_res.json()
            disease = diagnosis_data.get('disease', 'Unknown Condition')
            
            # Step 3: Recommendation (Layer 4)
            r_res = await client.get(f"http://localhost:8003/recommend/{disease}")
            rec_data = r_res.json()

            # Step 4: Gemini RAG Synthesis (Layer 5)
            rag_output = synthesize_rag_response(
                user_query=user_query,
                triage_symptoms=symptoms,
                ml_disease=disease,
                rec_data=rec_data
            )
            
            res = {
                "reply": rag_output.get("synthesized_reply"),
                "recommended_doctor": rec_data.get('recommended_doctor'),
                "architecture_trace": {
                    "Layer_1_Gateway_Firewall": {
                        "port": 8000,
                        "status": "PASSED (Safe - No emergency)"
                    },
                    "Layer_2_Triage_Service": {
                        "port": 8001,
                        "status": "COMPLETED",
                        "output_symptoms": symptoms
                    },
                    "Layer_3_Diagnosis_Service": {
                        "port": 8002,
                        "status": "COMPLETED",
                        "predicted_disease": disease,
                        "ml_model": "RandomForestClassifier"
                    },
                    "Layer_4_Recommendation_Service": {
                        "port": 8003,
                        "status": "COMPLETED",
                        "specialist": rec_data.get('recommended_doctor'),
                        "precautions": rec_data.get('precautions')
                    },
                    "Layer_5_RAG_Synthesizer": {
                        "status": rag_output.get("rag_status"),
                        "model": rag_output.get("model_used"),
                        "augmented_context_sources": ["spaCy NLP", "RandomForest ML", "CSV Datasets"]
                    }
                },
                "details": rec_data
            }
        except Exception as e:
            logging.error(f"Service Failure: {e}")
            res = {
                "reply": "I'm having trouble connecting to my diagnostic modules, but please consult a General Physician.",
                "recommended_doctor": "General Physician",
                "details": {"error": f"Handshake Failure: {str(e)}"}
            }

        chat_memory.append({"q": user_query, "a": res.get('reply')})
        return res