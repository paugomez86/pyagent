import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from helpers import generate_content
from functions.call_function import call_function
from config import MAX_MODEL_LOOP

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
    
    # Message list. Will contain all the content from the interaction with the LLM. Context, messages and function calls
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    
    # Setting a maximum number of LLM operations to avoid the agent to run indefinitely (and burn tokens)
    for _ in range(MAX_MODEL_LOOP):
        try:
            # Send prompt request
            response = generate_content(client, messages)
        except RuntimeError as e:
            print(f"Error getting API response: {e}")

        # Print user prompt and token usage if verbose
        if args.verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
        
        # Appending content of each response to message list
        if response.candidates is not None:
            for item in response.candidates:
                messages.append(item.content)
        
        # Running function calls provided by the LLM if there are any
        if response.function_calls is not None:
            # List where function results will be added
            function_call_results = []
            
            for function_call in response.function_calls:
                # Calling function
                function_call_result = call_function(function_call, args.verbose)
                
                # Catching and checking result
                # .parts should be a non-empty list
                if len(function_call_result.parts) == 0:
                    raise Exception(f"Error: {function_call.name}({function_call.args}) returned an empty list")
                # .parts[0].function_response should be a FunctionResponse object
                if function_call_result.parts[0].function_response is None:
                    raise Exception(f"Error: {function_call.name}({function_call.args}) returned an invalid or empty value")
                # .response is where the result of the function called should be
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception(f"Error: {function_call.name}({function_call.args}) returned no response")
                
                # This is where the results of correctly called and returned function calls are stored
                function_call_results.append(function_call_result.parts[0])
                
                # Print function call info and results if verbose
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # Appending function call results to message list
                messages.append(types.Content(role="user", parts=function_call_results))    
            
        # Otherwise printing plain text response
        # This is used to catch and print the final response to the user when the model has finished the task
        else:
            print("Final response:")
            print(f"{response.text}")
            return 0
        
    # In case the max specified iterations are run
    print(f"Program interrupted: Max model iterations ({MAX_MODEL_LOOP}) reached")
    return 1

if __name__ == "__main__":
    main()
    