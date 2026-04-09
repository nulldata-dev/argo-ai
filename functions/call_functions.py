from functions.get_files_info import *
from google.genai import types

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)