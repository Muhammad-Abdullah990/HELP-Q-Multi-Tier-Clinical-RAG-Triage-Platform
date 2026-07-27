def generate_response(predictions, doctor):
    if not predictions:
        return "Please provide more details."

    top = predictions[0]

    return f"""
🧠 Possible Condition: {top['disease']} ({round(top['confidence']*100,2)}%)

👨‍⚕️ Recommended: {doctor}

⚠ This is NOT a medical diagnosis. Please consult a doctor.
"""