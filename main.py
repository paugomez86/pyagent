import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from helpers import generate_content

from functions.get_files_info import get_files_info

def main():
    # Load environment
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("unable to import api key")
    
    # Instante api client
    client = genai.Client(api_key=api_key)
    
    # Setting argument parser
    parser = argparse.ArgumentParser(description="Gemini LLM powered chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("-V", "--verbose", action="store_true", help="Enable verbose output")

    # Catch prompt argument
    args = parser.parse_args()
    prompt = args.user_prompt
    
    # Message list
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    
    # Send prompt request
    try:
        response = generate_content(client, messages)
    except RuntimeError as e:
        print(f"Error getting API response: {e}")
    
    # Print user prompt and token usage if verbose
    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
    
    # Printing function calls if there are any
    if response.function_calls is not None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        # Printing plain text response
        print(f"{response.text}")
    

if __name__ == "__main__":
    main()
    