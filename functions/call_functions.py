from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *
from google.genai import types

WORKING_DIR = "./calculator" #the working directory used in call_function

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ],
)

def call_function(function_call, verbose=False):  #function_call is types.FunctionCall with name and args properties
    if verbose == True: #check for verbose flag
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    function_map = { #holds the possible function calls
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "run_python_file" : run_python_file,
        "write_file" : write_file,
    }

    function_name = function_call.name or "" #store the function_call.name in a variable, if None stores empty string

    if function_name not in function_map: #check if function being called is in the list
        return types.Content( #returns a types.Content object explaining the error
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},                    
                )
            ],
        )
    
    args = dict(function_call.args) if function_call.args else {} #make a shallow copy of function_call.args if it exists, if not create an empty dict
    args["working_dir"] = WORKING_DIR #assign the working dir
    function_result = function_map[function_name](**args) #call the function and capture the result

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )