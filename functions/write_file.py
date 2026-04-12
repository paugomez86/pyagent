import os

def write_file(working_directory, file_path, content):
    try:
        # Getting absolute paths
        working_abs = os.path.normpath(os.path.abspath(working_directory))
        file_abs = os.path.normpath(os.path.join(working_abs, file_path))
        
        # Checking target file is into the working folder boundary for security reasons
        if not os.path.commonpath([working_abs, file_abs]) == working_abs:
            return f'Error: Cannot write to "{file_abs}" as it is outside the permitted working directory'
        
        # Checking the target file is not a folder
        if os.path.isdir(file_abs):
            return f'Error: Cannot write to "{file_abs}" as it is a directory'
        
        # Creating the necessary parent folders for the file in case they don't exist
        os.makedirs(os.path.dirname(file_abs), exist_ok=True)
        
        # Opening file in write mode and adding content
        file = open(file_abs, "w")
        file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"