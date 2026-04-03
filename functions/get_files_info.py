import os

def get_files_info(working_dir, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_dir) #absolute path from relative path, based off the user set working directory
    except:
        return f'Error: Could not get abspath of "{working_dir}"'
    
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory)) #normalized, joined path to the target directory

    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir #check if the target dir is within the working dir
    valid_input_dir = os.path.isdir(target_dir) #check if the target dir is a valid directory

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not valid_input_dir:
        return f'Error: "{directory}" is not a directory'
    
    try:
        items_in_dir = os.listdir(target_dir)
    except:
        return f'Error: os.listdir failed on "{target_dir}"'
    
    files_info = []

    for item in items_in_dir:
        try:
            item_path = os.path.normpath(os.path.join(target_dir, item))
        except:
            return f'Error: item_path failed on "{item}"'
        try:
            item_size = os.path.getsize(item_path)
        except:
            return f'Error: item_size failed on "{item}"'
        try:
            item_is_dir = os.path.isdir(item_path)
        except:
            return f'Error: item_is_dir failed on "{item}"'
        
        files_info.append(f'{item}: file_size={item_size} bytes, is_dir={item_is_dir}')
    
    return "\n".join(files_info)