import os
from google.genai import types
import subprocess

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="""
    Takes 2 arguments, file_path and args. 
    You supply the file path to a python file you want to run, followed by any arguments.
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""
                The path to the python file you want to run.
                The path is relative to the working directory, a variable not in your control for security reasons.
                """,
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="""
                Any arguments you want the subprocess.run() to use.
                This should be an array of strings, each string being its own arguement.
                """,
            ),
        },
        required=["file_path"], #tells the llm what arguments are required.
    ),
)

def run_python_file(working_dir, file_path, args=None):
    abs_working_dir = os.path.abspath(working_dir) #abs path for working directory
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path)) #abs path for the file_path

    valid_target_dir = os.path.commonpath([abs_file_path, abs_working_dir]) == abs_working_dir
    if not valid_target_dir: #check if file_path is within the working directory 
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    valid_file = os.path.isfile(abs_file_path)
    if not valid_file: #check if file_path leads to a valid file
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if file_path[-3:] != '.py': #check the end of the file path to see if it is .py
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", abs_file_path] #create the command

    if args:
        command.extend(args) #add user args

    try:
        process_output = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
    except Exception as e: #catch any errors and return a string
        return f'Error: executing Python file: {e}'

    output_string = '' #the output of the function
    std_out = process_output.stdout #store the standard out of the subprocess.run
    std_err = process_output.stderr #store the error output of the subprocess.run
    
    try:
        if std_out != '': #add the output of subprocess.run stdout to the output string
            output_string += f'STDOUT: {std_out}\n'
        if std_err != '': #add the output of subprocess.run stderr to the output string
            output_string+= f'STDERR: {std_err}\n'
        if std_out == '' and std_err == '': #if neither had any output this will be added instead
            output_string+= 'No output produced\n'

        if process_output.returncode != 0: #if the process had a non zero return code append it to the output string
            output_string += f'Process exited with code {process_output.returncode}'
    except Exception as e: #catch any errors and return a string
        return f'Error: executing Python file: {e}'

    return output_string #if all goes well return a string with the output of the python subprocess