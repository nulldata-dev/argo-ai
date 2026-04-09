import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration( #function declaration for the LLM to understand what get_files_info does a function
    name="get_files_info", #name of the function
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status", #a short description for the LLM
    parameters=types.Schema( #the parameters of the function that the LLM has access to
        type=types.Type.OBJECT, #not sure ngl this is just what the docs say to do
        properties={ #explicit description of paremeters of the function
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_dir, directory="."):
    abs_working_dir = os.path.abspath(working_dir) #absolute path from relative path, based off the user set working directory
    
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory)) #normalized, joined path to the target directory

    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir 
    if not valid_target_dir: #check if the target dir is within the working dir
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    valid_input_dir = os.path.isdir(target_dir) 
    if not valid_input_dir: #check if the target dir is a valid directory
        return f'Error: "{directory}" is not a directory'

    try: #make a list of items in target_dir
        items_in_dir = os.listdir(target_dir)
    except: #catch any errors and return a string
        return f'Error: os.listdir failed on "{target_dir}"'
    
    files_info = [] #output list

    for item in items_in_dir:
        try: #get abs path of item
            item_path = os.path.normpath(os.path.join(target_dir, item))
        except: #catch any errors and return a string
            return f'Error: item_path failed on "{item}"'
        try: #get size of item in bytes
            item_size = os.path.getsize(item_path)
        except: #catch any errors and return a string
            return f'Error: item_size failed on "{item}"'
        try: #check if item is a directory
            item_is_dir = os.path.isdir(item_path)
        except: #catch any errors and return a string
            return f'Error: item_is_dir failed on "{item}"'
        
        files_info.append(f'{item}: file_size={item_size} bytes, is_dir={item_is_dir}') #add item to output list
    
    return "\n".join(files_info) #return output list as a string separated by newline chars