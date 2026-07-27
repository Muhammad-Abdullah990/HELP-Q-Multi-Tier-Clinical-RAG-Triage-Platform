import joblib
from shared.utils import log

model = joblib.load("model.pkl")

def predict(symptom_vector):
    log("Running prediction...")

    probs = model.predict_proba([symptom_vector])[0]
    classes = model.classes_

    results = sorted(
        zip(classes, probs),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    return results