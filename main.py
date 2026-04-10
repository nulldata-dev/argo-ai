import os
import sys
from config import *
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.call_functions import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose = False

    if len(sys.argv) < 2: #make sure the user inputs at least 1 input
        print("WARNING: Please provide a prompt!")
        exit(code=1)

    user_prompt = sys.argv[1] #set the user prompt to be the first command line argument

    messages = [ #turn the user prompt into a Content type for genai
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content( #make a call to genai to generate a response
        model=AI_MODEL, #set the model used to the value set in config.py
        contents=messages, #add the messages from the user
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, #include the system prompt
            tools=[available_functions], #pass the list of available functions and their declerations from call_functions.py
            temperature=0 #lower temperature == more deterministic
        ), 
    )     

    if len(sys.argv) > 1:
        for argument in sys.argv[1:]: #for every argument after the first
            if argument in ("--verbose", "-v"): #check if the user triggered the verbose flag
                verbose = True
    
    function_results = [] #stores results of function calls

    if response.function_calls is not None: #if the response contains function calls iterate on the list
        for function_call in response.function_calls: #iterate through function calls in the response
            function_call_result = call_function(function_call) #store the result of the function call
            if not function_call_result.parts:
                raise Exception(f'{function_call} had no .parts')
            if not function_call_result.parts.function_response:
                raise Exception(f'{function_call} had no function_reponse')
            if not function_call_result.parts.function_response.response:
                raise Exception(f'{function_call} had no result')
            function_results.append(function_call_result.parts[0])
            if verbose == True:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else: #if there are no function calls print the response
        print(response.text)

    if verbose == True:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
