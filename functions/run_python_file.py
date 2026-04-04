import os
import subprocess

def run_python_file(working_dir, file_path, args=None):
    abs_working_dir = os.path.abspath(working_dir) #abs path for working directory
    abs_file_path = os.path.join(abs_working_dir, file_path) #abs path for the file_path

    valid_target_dir = os.path.commonpath([abs_file_path, abs_working_dir]) == abs_working_dir
    if not valid_target_dir: #check if file_path is within the working directory 
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    valid_file = os.path.isfile(abs_file_path)
    if not valid_file: #check if file_path leads to a valid file
        return f'Error: File not found or is not a regular file: "{abs_file_path}"'
    
    if file_path[-3:] != '.py': #check the end of the file path to see if it is .py
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", abs_file_path] #create the command
    command.extend(args) #add user args

    try:
        process_output = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
    except Exception as e:
        return f'Error: executing Python file: {e}'

    output_string = ''
    std_out = process_output.stdout
    std_err = process_output.stderr
    
    try:
        if std_out != '':
            output_string += f'STDOUT: {std_out}\n'
        if std_err != '':
            output_string+= f'STDERR: {std_err}\n'
        if std_out == '' and std_err == '':
            output_string+= 'No output produced\n'

        if process_output.returncode != 0:
            output_string += f'Process exited with code {process_output.returncode}'
    except Exception as e:
        return f'Error: executing Python file: {e}'

    return output_string    