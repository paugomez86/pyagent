from config import DEFAULT_WORKING_DIRECTORY
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

# Available functions list. Getting values from schemas in each function file
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content, 
        schema_write_file, 
        schema_run_python_file
    ],
)

# Function to actually call functions from LLM response.
# function_call is a types.FunctionCall object. It gets a function name and a list of args
def call_function(function_call, verbose=False):
    # Printing additional function info if verbose is True
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    # Dict of valid functions. The values are actual callable functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    
    # Getting function name or empty if None
    function_name = function_call.name or ""
     
    # Returning types.Content object to describe the error in case the provided function by LLM is not on the list
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ],
        )
    
    # Getting args from function_call or empty if None
    args = dict(function_call.args) if function_call.args else {}
    
    # Adding working directory argument. This is manually provided aside from the LLM response
    args["working_directory"] = DEFAULT_WORKING_DIRECTORY
    
    # Calling function inside the function map
    result = function_map[function_name](**args)
    
    # Returning types.Content object to describe the result of the function
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ]
    )