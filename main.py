import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

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
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
