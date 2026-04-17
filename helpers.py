from google.genai import types
from functions.call_function import available_functions

def generate_content(client, messages):
    model = "gemini-2.5-flash"
    
    # Temperature sets the level of determinism. 0 is max
    temperature = 1.0
    
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=get_system_prompt(),
            temperature=temperature
        )
    )
    
    if response.usage_metadata.prompt_token_count is None or response.usage_metadata.candidates_token_count is None:
        raise RuntimeError("invalid response")
    return response

def get_system_prompt():
    default = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read the content of files
        - Write content to files
        - Run Python scripts. Files ended with .py

        All paths you provide should be relative to the working directory. 
        You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    return default