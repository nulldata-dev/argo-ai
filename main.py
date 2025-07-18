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

    if len(sys.argv) < 2: #make sure the user inputs at least 1 input
        print("WARNING: Please provide a prompt!")
        exit(code=1)

    user_prompt = sys.argv[1] #set the user prompt to be the first command line argument

    messages = [ #turn the user prompt into a Content type for genai
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content( #make a call to genai to generate a response
        model=AI_MODEL, contents=messages)      
        
    
    print(response.text)

    if len(sys.argv) > 1:
        for argument in sys.argv[1:]: #for every argument after the first
            if argument == "--verbose": #check if the user 
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
