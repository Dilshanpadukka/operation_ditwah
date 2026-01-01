import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_stress_test(scenario_text, temp):
    prompt = f"""
    Analyze the following crisis scenario. 
    Think step-by-step (Chain of Thought) and decide the immediate action.
    
    Scenario: {scenario_text}
    
    Plan:
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def main():
    input_path = os.path.join('data', 'scenarios.txt')
    if not os.path.exists(input_path):
        print("Scenarios file not found.")
        return

    with open(input_path, 'r') as f:
        # Split file by "SCENARIO" keyword to get blocks
        content = f.read()
        scenarios = ["SCENARIO" + s for s in content.split("SCENARIO") if s.strip()]

    print("--- Part 2: Stability Experiment ---")
    
    for i, scen in enumerate(scenarios):
        print(f"\nProcessing Scenario {i+1}...")
        
        # [cite_start]Chaos Mode (Temp 1.0) - Run 3 times [cite: 70]
        print(">>> CHAOS MODE (Temp 1.0)")
        for j in range(3):
            result = run_stress_test(scen, 1.0)
            print(f"[Run {j+1}]: {result[:150].replace(chr(10), ' ')}...") 
            
        # [cite_start]Safe Mode (Temp 0.0) - Run 1 time [cite: 71]
        print(">>> SAFE MODE (Temp 0.0)")
        result_safe = run_stress_test(scen, 0.0)
        print(f"[Safe Run]: {result_safe[:150].replace(chr(10), ' ')}...")

if __name__ == "__main__":
    main()