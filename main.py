import os
from constants import *
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=AI_MODEL, contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    
    print(response.text)



if __name__ == "__main__":
    main()
