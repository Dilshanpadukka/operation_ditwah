import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def main():
    input_path = os.path.join('data', 'incidents.txt')
    if not os.path.exists(input_path):
        print("Incidents file not found.")
        return

    with open(input_path, 'r') as f:
        incidents_text = f.read()

    # [cite_start]Step A: CoT Scoring [cite: 78]
    print("--- Part 3: Logistics Commander ---")
    print("Step A: Calculating Priority Scores...")
    
    score_prompt = f"""
    Analyze these incidents row by row. Assign a Priority Score (1-10) based on:
    - Base Score: 5
    - +2 if Age > 60 or < 5
    - +3 if Need == "Rescue" (Life Threat)
    - +1 if Need == "Insulin/Medicine"

    Incidents:
    {incidents_text}

    Provide the logic and final score for each.
    """
    
    scores_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[{"role": "user", "content": score_prompt}],
        temperature=0
    )
    scores = scores_response.choices[0].message.content
    print(f"\nSCORES:\n{scores}")

    # [cite_start]Step B: ToT Strategy [cite: 86]
    print("\nStep B: Determining Logistics Strategy (ToT)...")
    tot_prompt = f"""
    You are the Logistics Commander.
    Resources: ONE rescue boat at Ragama.
    Travel Times: Ragama->Ja-Ela (10m), Ja-Ela->Gampaha (40m).
    
    Analysis of Incidents:
    {scores}

    [cite_start]Evaluate 3 branches[cite: 89]:
    1. Greedy: Save highest score first.
    2. Speed: Save closest first.
    3. Logistics: Save furthest first.

    Goal: Maximize total priority score saved in shortest time.
    Select the optimal route and explain why.
    """

    strategy_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": tot_prompt}],
        temperature=0
    )

    strategy = strategy_response.choices[0].message.content
    print(f"\nOPTIMAL STRATEGY:\n{strategy}")

if __name__ == "__main__":
    main()