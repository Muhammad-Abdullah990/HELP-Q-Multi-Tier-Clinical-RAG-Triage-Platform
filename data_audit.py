import pandas as pd
import os

def perform_audit():
    print("--- 🔍 HELP-Q DATA INTELLIGENCE REPORT ---")
    files = {
        "Main Dataset": "datasets/dataset.csv",
        "Descriptions": "datasets/symptom_Description.csv",
        "Precautions": "datasets/symptom_precaution.csv",
        "Severity": "datasets/Symptom_severity.csv"
    }

    for name, path in files.items():
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"\n📂 {name.upper()}")
            print(f"- Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
            print(f"- Columns Found: {list(df.columns)}")
            
            # Identify Key Metrics (KPIs)
            if 'Disease' in df.columns:
                unique_diseases = df['Disease'].nunique()
                print(f"- Unique Diseases Covered: {unique_diseases}")
            
            # Topic Modeling (Top Symptoms)
            if name == "Main Dataset":
                # Get frequency of symptoms (non-zero entries)
                symptom_freq = df.iloc[:, 1:].notnull().sum().sort_values(ascending=False).head(5)
                print(f"- Top 5 Most Frequent Symptoms (Keyword Extraction):")
                for sym, freq in symptom_freq.items():
                    print(f"  > {sym}: {freq} occurrences")
        else:
            print(f"❌ MISSING FILE: {path}")

if __name__ == "__main__":
    perform_audit()