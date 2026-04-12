import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        # Getting absolute paths
        working_abs = os.path.normpath(os.path.abspath(working_directory))
        file_abs = os.path.normpath(os.path.join(working_abs, file_path))
        
        # Checking target file is into the working folder boundary for security reasons
        if not os.path.commonpath([working_abs, file_abs]) == working_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Checking the target file is actually a file
        if not os.path.isfile(file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        # Checking if the target file is a Python file
        if not file_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        # Building the command using the target file plus arguments
        command = ["python", file_abs]
        if args is not None:
            command.extend(args)
        
        # Running subprocess
        response = subprocess.run(command, text=True, timeout=30, capture_output=True)
        
        # Checking for failed return code
        if response.returncode != 0:
            return f'Process exited with code {response.returncode}'
        
        # Returning subrocess response
        if response.stderr == None and response.stdout == None:
            return f"No output produced"
        else:
            return f"STDOUT: {response.stdout}\nSTDERR:{response.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"