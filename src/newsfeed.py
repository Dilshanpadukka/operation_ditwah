import pandas as pd
import os
import json
from groq import Groq
from pydantic import BaseModel, ValidationError, Field
from typing import Optional, Literal
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# [cite_start]1. Define Schema [cite: 111]
class CrisisEvent(BaseModel):
    district: Literal['Colombo', 'Gampaha', 'Kandy', 'Kalutara', 'Galle', 'Matara', 'Nuwara Eliya', 'Ratnapura', 'Kegalle']
    flood_level_meters: Optional[float] = None
    victim_count: int = 0
    main_need: str
    status: Literal['Critical', 'Warning', 'Stable']

def main():
    input_path = os.path.join('data', 'news_feed.txt')
    output_path = os.path.join('output', 'flood_report.xlsx')

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    with open(input_path, 'r') as f:
        news_lines = f.readlines()

    feed_results = []
    print("--- Part 5: News Feed Extraction ---")
    
    for line in news_lines:
        line = line.strip()
        if not line or "[source" in line: continue

        # [cite_start]JSON Extraction Prompt [cite: 121]
        extract_prompt = f"""
        Extract the following crisis event into JSON format.
        Schema:
        - district: Must be one of: Colombo, Gampaha, Kandy, Kalutara, Galle, Matara, Nuwara Eliya, Ratnapura, Kegalle.
        - flood_level_meters: number or null.
        - victim_count: integer (default 0).
        - main_need: short string describing need.
        - status: Critical, Warning, or Stable.
        
        Input: "{line}"
        JSON:
        """
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": extract_prompt}],
                temperature=0,
                response_format={"type": "json_object"} 
            )
            
            json_str = response.choices[0].message.content
            
            # [cite_start]Validate [cite: 122]
            event = CrisisEvent.model_validate_json(json_str)
            feed_results.append(event.model_dump())
            print(f"[Valid]: {event.district} | {event.main_need}")
            
        except ValidationError as e:
            print(f"[Skip]: Validation Error -> {e}")
        except Exception as e:
            print(f"[Error]: API issue -> {e}")

    # [cite_start]Save to Excel [cite: 124]
    if feed_results:
        news_df = pd.DataFrame(feed_results)
        os.makedirs('output', exist_ok=True)
        news_df.to_excel(output_path, index=False)
        print(f"\nSuccess! Report saved to {output_path}")
    else:
        print("No valid data extracted.")

if __name__ == "__main__":
    main()