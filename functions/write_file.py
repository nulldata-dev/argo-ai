import os

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