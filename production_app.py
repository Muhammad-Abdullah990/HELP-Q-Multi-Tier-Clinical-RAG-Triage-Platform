import os
import sys
import importlib.util
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add directory to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from shared.rag_engine import synthesize_rag_response

# Load individual microservice modules
def load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

chat_mod = load_module("chat_mod", os.path.join(os.path.dirname(__file__), "chat-service", "app.py"))
triage_mod = load_module("triage_mod", os.path.join(os.path.dirname(__file__), "triage-service", "app.py"))
diagnosis_mod = load_module("diagnosis_mod", os.path.join(os.path.dirname(__file__), "diagnosis-service", "app.py"))
recommendation_mod = load_module("recommendation_mod", os.path.join(os.path.dirname(__file__), "recommendation-service", "app.py"))

app = FastAPI(
    title="H.E.L.P-Q Unified Production Microservice Platform",
    version="1.0.0"
)

# Enable CORS for Production Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Sub-Applications for documentation
app.mount("/gateway", chat_mod.app)
app.mount("/service/triage", triage_mod.app)
app.mount("/service/diagnosis", diagnosis_mod.app)
app.mount("/service/recommendation", recommendation_mod.app)

@app.get("/")
async def root():
    return {
        "system": "H.E.L.P-Q Unified Production Microservice Platform",
        "developer": "Eng. Mohammad Abdullah",
        "status": "Operational",
        "profiles": {
            "linkedin": "https://www.linkedin.com/in/eng-mohammad-abdullah/",
            "whatsapp": "https://wa.me/923196387153",
            "upwork": "https://www.upwork.com/freelancers/~01e0d1acd3e98b3d1f?mp_source=share"
        },
        "services": {
            "gateway": "/gateway/chat",
            "triage": "/service/triage/triage",
            "diagnosis": "/service/diagnosis/diagnose",
            "recommendation": "/service/recommendation/recommend/{disease}"
        },
        "docs": "/docs"
    }

@app.get("/developer")
@app.get("/author")
async def get_developer_info():
    return {
        "developer": "Eng. Mohammad Abdullah",
        "title": "Lead AI & Microservices Architect",
        "verification": "Verified Sole Author & Architect of H.E.L.P-Q Engine",
        "profiles": {
            "linkedin": "https://www.linkedin.com/in/eng-mohammad-abdullah/",
            "whatsapp": "https://wa.me/923196387153",
            "upwork": "https://www.upwork.com/freelancers/~01e0d1acd3e98b3d1f?mp_source=share"
        }
    }

# Optimized In-Process Production Pipeline (Zero-Latency, No HTTP Deadlocks on Render!)
@app.post("/chat")
async def chat_production(user_query: str):
    q_lower = user_query.lower()

    # Layer 1: Firewall Check
    emergency_keywords = ["chest pain", "breath", "unconscious", "bleeding"]
    if chat_mod.contains_word(q_lower, emergency_keywords):
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
    if chat_mod.contains_word(q_lower, support_keywords):
        return {
            "reply": "I am the H.E.L.P-Q Engine engineered by Eng. Mohammad Abdullah. I process symptoms through spaCy NLP triage, Random Forest ML prediction, and Gemini RAG synthesis to route you to the correct specialist.",
            "recommended_doctor": "System Support",
            "architecture_trace": {
                "Layer_1_Gateway_Firewall": {"port": 8000, "status": "SUPPORT_MODE", "action": "System Information"},
                "Layer_2_Triage_Service": {"port": 8001, "status": "NOT_NEEDED"},
                "Layer_3_Diagnosis_Service": {"port": 8002, "status": "NOT_NEEDED"},
                "Layer_4_Recommendation_Service": {"port": 8003, "status": "NOT_NEEDED"},
                "Layer_5_RAG_Synthesizer": {"status": "NOT_NEEDED"}
            },
            "details": {
                "developer": "Eng. Mohammad Abdullah",
                "status": "Operational"
            }
        }

    # In-Process Microservice Pipeline Execution
    try:
        # Step 1: Triage (Layer 2)
        triage_res = await triage_mod.triage(text=user_query)
        symptoms = triage_res.get('symptoms', [])

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
        input_obj = diagnosis_mod.SymptomInput(symptoms=symptoms)
        diag_res = await diagnosis_mod.diagnose(input_data=input_obj)
        disease = diag_res.get('disease', 'Unknown Condition')

        # Step 3: Recommendation (Layer 4)
        rec_res = await recommendation_mod.recommend(disease=disease)

        # Step 4: Gemini RAG Synthesis (Layer 5)
        rag_output = synthesize_rag_response(
            user_query=user_query,
            triage_symptoms=symptoms,
            ml_disease=disease,
            rec_data=rec_res
        )

        return {
            "reply": rag_output.get("synthesized_reply"),
            "recommended_doctor": rec_res.get('recommended_doctor'),
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
                    "specialist": rec_res.get('recommended_doctor'),
                    "precautions": rec_res.get('precautions')
                },
                "Layer_5_RAG_Synthesizer": {
                    "status": rag_output.get("rag_status"),
                    "model": rag_output.get("model_used"),
                    "augmented_context_sources": ["spaCy NLP", "RandomForest ML", "CSV Datasets"]
                }
            },
            "details": rec_res
        }
    except Exception as e:
        return {
            "reply": "I'm having trouble connecting to my diagnostic modules, but please consult a General Physician.",
            "recommended_doctor": "General Physician",
            "details": {"error": f"Execution Error: {str(e)}"}
        }
