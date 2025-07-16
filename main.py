import os
import sys
from constants import *
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    if len(sys.argv) > 1:
        response = client.models.generate_content(
            model=AI_MODEL, contents=messages)      
    else:
        print("WARNING: Please provide a prompt!")
        exit(code=1)
    
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
