import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.utils import log

def train_model():
    log("Starting Advanced Training with Wide-Format Data...")
    df = pd.read_csv('../datasets/dataset.csv')
    
    # Clean whitespace from symptom names
    for col in df.columns:
        if col != 'Disease':
            df[col] = df[col].str.replace('_', ' ').str.strip()

    # Get a unique list of all possible symptoms across all 17 columns
    all_symptoms = pd.unique(df.iloc[:, 1:].values.ravel('K'))
    all_symptoms = [s for s in all_symptoms if str(s) != 'nan']
    
    # Create a new "Binary" dataframe (One-Hot Encoding)
    # This transforms your data so the AI sees "Fever: 1, Headache: 0"
    binary_data = pd.DataFrame(0, index=df.index, columns=all_symptoms)
    for i in range(len(df)):
        row_symptoms = df.iloc[i, 1:].values
        for s in row_symptoms:
            if str(s) != 'nan':
                binary_data.at[i, s] = 1
                
    X = binary_data
    y = df['Disease'].str.strip()
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, 'model.pkl')
    joblib.dump(all_symptoms, 'columns.pkl')
    log(f"Training Complete. Captured {len(all_symptoms)} unique symptoms.")

if __name__ == "__main__":
    train_model()