import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[RAG ENGINE] Warning initializing Gemini Client: {e}")

def synthesize_rag_response(user_query: str, triage_symptoms: list, ml_disease: str, rec_data: dict) -> dict:
    description = rec_data.get("description", "")
    precautions = rec_data.get("precautions", [])
    specialist = rec_data.get("recommended_doctor", "General Physician")
    
    augmented_prompt = f"""
You are the clinical AI assistant for H.E.L.P-Q (Healthcare Expert Location & Patient-triage System).
A patient provided the following symptom query: "{user_query}"

RETRIEVED CLINICAL CONTEXT:
1. spaCy NLP Extracted Symptoms: {', '.join(triage_symptoms) if triage_symptoms else 'None'}
2. Machine Learning (RandomForest) Predicted Disease: {ml_disease}
3. Recommended Medical Specialist: {specialist}
4. Clinical Description: {description}
5. Care Precautions: {', '.join(precautions) if precautions else 'None'}

INSTRUCTIONS:
- Synthesize an empathetic, clear, patient-friendly response explaining what their symptoms resemble based on the retrieved data.
- Explicitly account for any linguistic negations in the user query (e.g. if they said "without fever" or "no rash", clarify that those were ruled out).
- Include the specialist doctor recommendation and actionable care precautions.
- End with a mandatory medical disclaimer stating that this is an AI-assisted decision support system and not a final medical diagnosis.
- Keep the response structured, clear, and reassuring (2-3 short paragraphs).
"""

    if not client:
        return {
            "synthesized_reply": f"Based on the clinical analysis, your symptoms resemble {ml_disease}. We recommend consulting a {specialist}.",
            "rag_status": "FALLBACK_NO_API_KEY",
            "model_used": "Template Fallback Engine"
        }

    # Try Primary Models
    for model_name in ['gemini-1.5-flash', 'gemini-2.0-flash', 'gemini-1.5-pro']:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=augmented_prompt
            )
            return {
                "synthesized_reply": response.text.strip(),
                "rag_status": "SUCCESS",
                "model_used": model_name
            }
        except Exception as e:
            err_msg = str(e)
            print(f"[RAG ENGINE] Model {model_name} failed: {err_msg[:100]}")
            continue

    # Clean Fallback if free tier API rate limit / 429 occurs
    return {
        "synthesized_reply": f"Based on the analysis of your symptoms, the condition resembles {ml_disease}. We recommend scheduling a consultation with a {specialist}.\n\nKey Care Precautions:\n• " + "\n• ".join(precautions if precautions else ["Consult your primary care physician."]) + "\n\nDisclaimer: This is an AI decision support tool and not a final medical diagnosis.",
        "rag_status": "RATE_LIMITED_429 (Clinical Fallback Active)",
        "model_used": "Clinical Fallback Engine"
    }
