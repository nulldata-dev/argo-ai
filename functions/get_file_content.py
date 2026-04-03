import os
from config import *

def get_file_content(working_dir, file_path):
    abs_working_dir = os.path.abspath(working_dir) #abs path for working directory
    abs_file_path = os.path.join(abs_working_dir, file_path) #abs path for the file_path

    valid_target_dir = os.path.commonpath([abs_file_path, abs_working_dir]) == abs_working_dir
    if not valid_target_dir: #check if file_path is within the working directory 
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    valid_file = os.path.isfile(abs_file_path)
    if not valid_file: #check if file_path leads to a valid file
        return f'Error: File not found or is not a regular file: "{abs_file_path}"'
    
    try:
        with open(abs_file_path, "r") as file:
            try:
                file_content = file.read(MAX_CHARS)
            except:
                return f'Error: could not read "{abs_file_path}"'
            if file.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except:
        return f'Error: could not open "{abs_file_path}"'
    
    return file_content
        