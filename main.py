import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("gemini api key environment variable not found")
    
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata == None:
            raise RuntimeError("failed API request")
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if response.function_calls != None:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception("no parts returned")
                if not function_call_result.parts[0].function_response:
                    raise Exception("no function_response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("no function_response.response")
                
                function_results = [function_call_result.parts[0]]
                messages.append(types.Content(role="user", parts=function_results))

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                    

        else:
            print(response.text)
            sys.exit(0)

    print("max number of iterations reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
