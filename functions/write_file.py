import os
from google.genai import types

schema_write_file = types.FunctionDeclaration( #function declaration for the LLM to understand what get_files_info does a function
    name="write_file", #name of the function
    description="""
    Writes a file at a specified file_path with a given content.
    """, #a description of the function for the LLM
    parameters=types.Schema( #the parameters of the function that the LLM has access to
        type=types.Type.OBJECT, #not sure ngl this is just what the docs say to do
        properties={ #explicit description of paremeters of the function
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""
                The path to the file you want to write, relative to the user defined working directory.
                This can be a file that already exists but you will be overwriting it.
                The folders do not need to exist, the function will create anything in the file path that does not exist.
                Must be given, has no default value.
                """,
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="""
                The content you want to write to the file at the file_path.
                This will overwrite any existing data if there was any.
                Must be given, has no default value.
                """,
            ),
        },
    ),
)

def write_file(working_dir, file_path, content):
    abs_working_dir = os.path.abspath(working_dir) #absolute path to the working directory
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path)) #absolute path to the file

    valid_target_dir = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
    if not valid_target_dir: #check if file_path is within the working directory
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(abs_file_path): #check if the file path leads to 
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True) #make any dirs that do not exist
    except:
        return f'Error: could not makedirs for "{abs_file_path}"'
    
    try:
        with open(abs_file_path, "w") as file: #open the file in writing mode
            try:
                file.write(content) #replaces exisiting file or creates new file with content
            except:
                return f'Error: could not write "{file}"'
    except:
        return f'Error: could not open "{abs_file_path}"'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'