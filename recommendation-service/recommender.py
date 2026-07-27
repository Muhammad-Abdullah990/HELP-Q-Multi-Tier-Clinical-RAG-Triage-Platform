mapping = {
    "Fungal infection": "Dermatologist",
    "Allergy": "General Physician",
    "GERD": "Gastroenterologist",
    "Chronic cholestasis": "Hepatologist"
}

def recommend(disease):
    return mapping.get(disease, "General Physician")