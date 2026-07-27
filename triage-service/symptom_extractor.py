import pandas as pd
import spacy
from shared.utils import log

nlp = spacy.load("en_core_web_sm")

# Load symptoms dynamically from dataset
df = pd.read_csv("../datasets/dataset.csv")
SYMPTOMS = list(df.columns[:-1])  # all except prognosis

def extract(text):
    log("Extracting symptoms...")

    doc = nlp(text.lower())
    found = []

    for symptom in SYMPTOMS:
        if symptom.replace("_", " ") in text.lower():
            found.append(symptom)

    return found