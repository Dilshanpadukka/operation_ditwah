import os
import sys
from groq import Groq
from dotenv import load_dotenv

# Add parent dir to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.token_utils import count_tokens

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def summarize_message(text):
    # [cite_start]"""Uses Groq to summarize long messages[cite: 103]."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Summarize this crisis message briefly to save tokens."},
                {"role": "user", "content": text}
            ],
            max_tokens=50
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error summarizing"

def process_message_budget(message):
    # [cite_start]Logic: If > 150 tokens -> Truncate or Summarize [cite: 101]
    token_count = count_tokens(message)
    limit = 150
    
    print(f"Message Length: {len(message)} chars | Est Tokens: {token_count}")
    
    if token_count > limit:
        print(">> BLOCKED: Message too long. Summarizing...")
        summary = summarize_message(message)
        return f"SUMMARY: {summary}"
    
    return "PASSED: Token count within limits."

def main():
    # Test Data
    long_spam = "Urgent attention required regarding the recent flood " * 40 # Creates ~200+ tokens
    short_msg = "Help us! We are stuck in Ja-Ela."

    print("--- Part 4: Budget Keeper ---")
    print("\n[Test 1: Long Message]")
    print(process_message_budget(long_spam))
    
    print("\n[Test 2: Short Message]")
    print(process_message_budget(short_msg))

if __name__ == "__main__":
    main()