import os
from google.genai import types

# Schema for writing to a file. It tells the LLM how to use the function. Function below
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to the given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the target file to write the content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content in text format that will be written to the target file",
            )
        },
        required=["file_path", "content"],
    ),
)

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