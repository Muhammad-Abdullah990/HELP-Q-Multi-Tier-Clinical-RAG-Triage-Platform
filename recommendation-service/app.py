import os
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
desc_df = pd.read_csv(os.path.join(BASE_DIR, '../datasets/symptom_Description.csv'))
prec_df = pd.read_csv(os.path.join(BASE_DIR, '../datasets/symptom_precaution.csv'))

@app.get("/")
async def root():
    return {
        "service": "H.E.L.P-Q Recommendation Service",
        "status": "Operational",
        "port": 8003,
        "docs": "http://127.0.0.1:8003/docs",
        "endpoint": "GET /recommend/{disease}"
    }

DOCTOR_MAP = {
    "Fungal infection": "Dermatologist", "Allergy": "Allergist / Immunologist",
    "GERD": "Gastroenterologist", "Chronic cholestasis": "Hepatologist",
    "Drug Reaction": "Allergist", "Peptic ulcer diseae": "Gastroenterologist",
    "AIDS": "Infectious Disease Specialist", "Diabetes": "Endocrinologist",
    "Gastroenteritis": "Gastroenterologist", "Bronchial Asthma": "Pulmonologist",
    "Hypertension": "Cardiologist", "Migraine": "Neurologist",
    "Cervical spondylosis": "Orthopedic Surgeon", "Paralysis (brain hemorrhage)": "Neurologist",
    "Jaundice": "Hepatologist", "Malaria": "Infectious Disease Specialist",
    "Chicken pox": "Pediatrician / Dermatologist", "Dengue": "Infectious Disease Specialist",
    "Typhoid": "Internal Medicine", "hepatitis A": "Hepatologist",
    "Hepatitis B": "Hepatologist", "Hepatitis C": "Hepatologist",
    "Hepatitis D": "Hepatologist", "Hepatitis E": "Hepatologist",
    "Alcoholic hepatitis": "Hepatologist", "Tuberculosis": "Pulmonologist",
    "Common Cold": "General Physician", "Pneumonia": "Pulmonologist",
    "Dimorphic hemmorhoids(piles)": "Proctologist", "Heart attack": "Cardiologist",
    "Varicose veins": "Vascular Surgeon", "Hypothyroidism": "Endocrinologist",
    "Hyperthyroidism": "Endocrinologist", "Hypoglycemia": "Endocrinologist",
    "Osteoarthristis": "Rheumatologist", "Arthritis": "Rheumatologist",
    "(vertigo) Paroymsal  Positional Vertigo": "ENT Specialist", "Acne": "Dermatologist",
    "Urinary tract infection": "Urologist", "Psoriasis": "Dermatologist",
    "Impetigo": "Dermatologist"
}

@app.get("/recommend/{disease}")
async def recommend(disease: str):
    desc_row = desc_df[desc_df['Disease'].str.strip() == disease.strip()]
    description = desc_row['Description'].values[0] if not desc_row.empty else "No description available."
    
    prec_row = prec_df[prec_df['Disease'].str.strip() == disease.strip()]
    precautions = []
    if not prec_row.empty:
        precautions = prec_row.iloc[0, 1:].dropna().tolist()
        
    specialist = DOCTOR_MAP.get(disease.strip(), "General Physician")
    
    return {
        "description": description,
        "precautions": precautions,
        "recommended_doctor": specialist
    }