from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content,
        schema_run_python_file,
    ],
)