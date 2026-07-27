import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add directories to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import individual microservice FastAPI apps
import importlib.util

def load_app(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app

chat_app = load_app("chat_app", os.path.join(os.path.dirname(__file__), "chat-service", "app.py"))
triage_app = load_app("triage_app", os.path.join(os.path.dirname(__file__), "triage-service", "app.py"))
diagnosis_app = load_app("diagnosis_app", os.path.join(os.path.dirname(__file__), "diagnosis-service", "app.py"))
recommendation_app = load_app("recommendation_app", os.path.join(os.path.dirname(__file__), "recommendation-service", "app.py"))

# Create Unified Production App
app = FastAPI(
    title="H.E.L.P-Q Unified Production Microservice Platform",
    version="1.0.0"
)

# Enable CORS for Production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Microservices
app.mount("/gateway", chat_app)
app.mount("/service/triage", triage_app)
app.mount("/service/diagnosis", diagnosis_app)
app.mount("/service/recommendation", recommendation_app)

@app.get("/")
async def root():
    return {
        "system": "H.E.L.P-Q Unified Production Microservice Platform",
        "status": "Operational",
        "services": {
            "gateway": "/gateway/chat",
            "triage": "/service/triage/triage",
            "diagnosis": "/service/diagnosis/diagnose",
            "recommendation": "/service/recommendation/recommend/{disease}"
        },
        "docs": "/docs"
    }

# Forward /chat directly to gateway chat for convenience
@app.post("/chat")
async def chat_forward(user_query: str):
    # Delegate directly to chat service
    async with chat_app.router.app(user_query):
        pass
