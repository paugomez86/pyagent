import os
from google.genai import types

# Schema for getting files from directory. It tells the LLM how to use the function. Function below
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        # Getting absolute paths
        working_abs = os.path.abspath(working_directory)
        directory_abs = os.path.normpath(os.path.join(working_abs, directory))
        
        # Checking if working folder and target folder exist
        if not os.path.exists(working_abs):
            return f'Error: "{working_abs}" is not a directory'
        if not os.path.exists(directory_abs):
            return f'Error: "{directory_abs}" is not a directory'

        # Check if target directory is in working directory for security reasons
        if not os.path.commonpath([working_abs, directory_abs]) == working_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Reading target folder contents and returning a list
        contents = ""
        for item in os.listdir(directory_abs):
            item_abs = os.path.abspath(os.path.join(directory_abs, item))
            contents += f"- {item}: file_size={os.path.getsize(item_abs)}, is_dir={os.path.isdir(item_abs)}\n"
        return contents.rstrip("\n")
    except Exception as e:
        return "Error: {e}"
    