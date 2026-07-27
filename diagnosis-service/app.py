import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Absolute path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
all_features = joblib.load(os.path.join(BASE_DIR, 'columns.pkl'))

@app.get("/")
async def root():
    return {
        "service": "H.E.L.P-Q Diagnosis Service",
        "status": "Operational",
        "port": 8002,
        "docs": "http://127.0.0.1:8002/docs",
        "endpoint": "POST /diagnose"
    }

# Define the expected data structure
class SymptomInput(BaseModel):
    symptoms: list

@app.post("/diagnose")
async def diagnose(input_data: SymptomInput):
    symptoms_list = input_data.symptoms
    input_df = pd.DataFrame(0, index=[0], columns=all_features)
    
    for s in symptoms_list:
        clean_s = s.lower().strip()
        for feature in all_features:
            if clean_s in feature.lower():
                input_df[feature] = 1
                
    prediction = model.predict(input_df)[0]
    return {"disease": prediction}