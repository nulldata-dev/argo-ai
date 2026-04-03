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
    
    try: #open the file at abs_file_path if it is a file
        with open(abs_file_path, "r") as file:
            file_content = file.read(MAX_CHARS) #read file content to the output string
            if file.read(1): #check if there is anything left in the buffer
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]' #inform user of truncation if present
    except: #return an error string if it fails
        return f'Error: could not open "{abs_file_path}"'
    
    return file_content #return file content
        