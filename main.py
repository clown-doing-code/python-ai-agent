import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion


def main()-> None:
    load_dotenv()
    api_key: str | None = os.environ.get("OPENROUTER_API_KEY")

    client: OpenAI = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[dict[str, str]] = [
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    generated_content(client, messages, args.verbose)

def generated_content(client: OpenAI, messages: list, verbose: bool)-> None:

    response: ChatCompletion = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
