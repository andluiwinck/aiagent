import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    print("Hello from Build an AI agent in Python!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            if response.candidates is not None:
                for candidate in response.candidates:
                    if candidate.content is not None:
                        messages.append(candidate.content)

            if not response.usage_metadata:
                raise RuntimeError("Gemini API response appears to be malformed")

            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )

            if not response.function_calls and response.text:
                print("Response:")
                print(response.text)
                return

            if response.function_calls:
                function_response_parts = []
                for function_call in response.function_calls:
                    function_call_result = call_function(
                        function_call, verbose=args.verbose
                    )
                    if (
                        not function_call_result.parts
                        or not function_call_result.parts[0].function_response
                        or function_call_result.parts[0].function_response.response
                        is None
                    ):
                        raise RuntimeError(
                            "Function call result missing function_response"
                        )
                    function_response_parts.append(function_call_result.parts[0])
                    if args.verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )

                messages.append(
                    types.Content(role="user", parts=function_response_parts)
                )
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == "__main__":
    main()
