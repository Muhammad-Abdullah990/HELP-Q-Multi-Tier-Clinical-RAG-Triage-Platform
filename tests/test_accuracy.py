import httpx
import asyncio
import pandas as pd

async def run_audit():
    test_cases = [
        {"input": "I have skin rash and itching", "expected": "Fungal infection", "type": "Medical"},
        {"input": "Chest pain and trouble breathing", "expected": "EMERGENCY", "type": "Safety"},
        {"input": "How does this system work?", "expected": "H.E.L.P-Q", "type": "Support"},
        {"input": "I am shivering and sneezing", "expected": "Allergy", "type": "Medical"}
    ]
    
    results = []
    async with httpx.AsyncClient() as client:
        for case in test_cases:
            resp = await client.post("http://localhost:8000/chat", params={"user_query": case['input']})
            data = resp.json()
            is_correct = case['expected'].lower() in str(data).lower()
            results.append({
                "Type": case['type'],
                "Query": case['input'],
                "Pass": "✅" if is_correct else "❌"
            })

    df = pd.DataFrame(results)
    print("\n--- 📊 H.E.L.P-Q FINAL QA REPORT ---")
    print(df.to_string(index=False))
    print(f"\nOverall Accuracy: {(df['Pass']=='✅').mean()*100:.2f}%")

if __name__ == "__main__":
    asyncio.run(run_audit())