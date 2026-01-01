import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def classify_message(message):
    # [cite_start]Few-Shot Prompting as per requirements [cite: 57]
    prompt = f"""
    You are a Crisis Intelligence System for Cyclone Ditwah. Classify the incoming message.
    
    Examples:
    Input: "Breaking News: Kelani River level at 9m."
    Output: District: Colombo | Intent: Info | Priority: Low

    Input: "We are trapped on the roof with 3 kids!"
    Output: District: Unknown | Intent: Rescue | Priority: High

    Input: "Gampaha hospital needs drinking water for patients."
    Output: District: Gampaha | Intent: Supply | Priority: High

    Input: "Just saw a movie, it was great."
    Output: District: None | Intent: Other | Priority: Low

    Input: "{message}"
    Output:
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    input_path = os.path.join('data', 'sample_messages.txt')
    output_path = os.path.join('output', 'classified_messages.xlsx')
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r') as f:
        raw_lines = f.readlines()

    results = []
    print("--- Part 1: Classifying Messages ---")
    for line in raw_lines:
        clean_line = line.strip()
        if clean_line: 
            classification = classify_message(clean_line)
            # Simple parsing for the DataFrame
            parts = classification.split('|')
            district = parts[0].split(':')[-1].strip() if len(parts) > 0 else "N/A"
            intent = parts[1].split(':')[-1].strip() if len(parts) > 1 else "N/A"
            priority = parts[2].split(':')[-1].strip() if len(parts) > 2 else "N/A"

            results.append({
                "Message": clean_line, 
                "Full_Output": classification,
                "District": district,
                "Intent": intent,
                "Priority": priority
            })
            print(f"Processed: {clean_line[:30]}...")

    df = pd.DataFrame(results)
    os.makedirs('output', exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"Success! Data saved to {output_path}")

if __name__ == "__main__":
    main()