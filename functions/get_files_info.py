import os

def get_files_info(working_directory, directory="."):
    path_to_directory = os.path.join(working_directory, directory)
    working_directory_abs = os.path.abspath(working_directory)
    target_dir_abs = os.path.abspath(path_to_directory)

    if not target_dir_abs.startswith(working_directory_abs): #make sure the 
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path_to_directory): #check if directory is a directory
        return f'Error: "{directory}" is not a directory'
    
    directory_contents = os.listdir(directory)
    dir_contents_string = ""

    for file in directory_contents: #loop through all files in the working dir
        path_to_file = os.path.join(working_directory, file)
        print(f"path_to_file: {path_to_file}")
        file_size = os.path.getsize(path_to_file)
        file_is_dir = os.path.isdir(path_to_file)
        dir_contents_string += f"- {file}: files_size={file_size}, is_dir={file_is_dir}\n"
    
    print(dir_contents_string)
    

get_files_info("~/workspace/github.com/nulldata-dev/argo-ai")