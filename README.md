# 🧠 H.E.L.P-Q AI — Medical Triage & Disease Prediction Platform

> **Healthcare Expert Location & Patient-Triage Engine**  
> *An Enterprise-grade, 5-Tier Microservice Platform combining spaCy NLP, RandomForest Machine Learning, and Google Gemini RAG (Retrieval-Augmented Generation).*

---

## 🌟 Key Architecture & Features

```
[Patient Query] ──► [Layer 1: Gateway Firewall] (Sub-5ms Emergency Escalation)
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
    [Emergency ER Warning]      [Layer 2: spaCy NLP Triage] (Token & POS Extraction)
                                          │
                                          ▼
                                [Layer 3: RandomForest ML] (131 Binary Feature Matrix)
                                          │
                                          ▼
                                [Layer 4: Recommendation Engine] (Specialist Doctor Routing)
                                          │
                                          ▼
                                [Layer 5: Gemini RAG Synthesizer] (Context Augmentation)
```

- **Layer 1 (Gateway & Safety Firewall)**: Zero-latency keyword detection for critical life safety (e.g., chest pain, breathing distress).
- **Layer 2 (spaCy NLP Triage)**: POS tag extraction filtering `NOUN` & `ADJ` clinical symptom tokens.
- **Layer 3 (Machine Learning Diagnosis)**: Multi-class `RandomForestClassifier` trained on 4,920 records across 131 symptom dimensions.
- **Layer 4 (Specialist & Care Router)**: Maps predicted diseases to 41 specialist doctor categories with 4-step care precautions.
- **Layer 5 (Gemini RAG Engine)**: Context-augmented LLM response synthesis with negation awareness and clinical disclaimers.
- **HCI React Dashboard**: Dark mode glassmorphic UI with real-time 4-Layer Architecture Inspector & Telemetry.

---

## 📁 Repository Structure

```
helpq-ai-system/
├── chat-service/           # Layer 1 Gateway & Main API Orchestrator
├── triage-service/         # Layer 2 spaCy NLP Symptom Extractor
├── diagnosis-service/      # Layer 3 RandomForest ML Engine (model.pkl)
├── recommendation-service/# Layer 4 Specialist & Care Precautions Router
├── shared/                 # Layer 5 Gemini RAG Synthesizer & Utils
├── datasets/               # Clinical datasets (Symptoms, Severity, Precautions)
├── frontend/               # React (Vite) HCI Glassmorphism Dashboard
├── production_app.py       # Unified Production Microservice Entrypoint
├── requirements.txt        # Backend dependencies
└── Procfile                # Render / Production deployment config
```

---

## 🚀 Local Development Setup

### 1. Backend Microservices
```bash
# Activate Virtual Environment
.venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Launch Unified Backend
uvicorn production_app:app --reload --port 8000
```

### 2. React Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit the HCI Dashboard at **`http://localhost:5173`**.

---

## 🔒 Copyright & Intellectual Property

**Copyright (c) 2026. All Rights Reserved.**

This repository and its source code are published for portfolio demonstration and educational review purposes only. **No permission is granted** for commercial reproduction, distribution, modification, or re-use without explicit written consent from the author.
