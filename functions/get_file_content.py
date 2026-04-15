import os
from config import MAX_CHARS
from google.genai import types

# Schema for getting content from a file. It tells the LLM how to use the function. Function below
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file in text format. The content is truncated if exceeds MAX_CHARS constant value",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the target file to get the content from, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        # Getting absolute paths
        working_abs = os.path.normpath(os.path.abspath(working_directory))
        file_abs = os.path.normpath(os.path.join(working_abs, file_path))
        
        # Checking target file is into the working folder boundary for security reasons
        if not os.path.commonpath([working_abs, file_abs]) == working_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Checking the target file exists
        if not os.path.exists(file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # File open in read mode and reading N max characters. Truncating if necessary
        file = open(file_abs, "r")
        file_content = file.read(MAX_CHARS)
        if file.read(1):
            file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return file_content
    except Exception as e:
        return f"Error: {e}"