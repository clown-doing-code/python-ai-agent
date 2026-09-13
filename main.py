import argparse
import os
from collections.abc import Iterable
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from config import MAX_ITERATIONS, SYSTEM_PROMPT
from functions.call_function import available_functions, call_function


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

    messages: Iterable[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    generated_content(client, messages, args.verbose)

def generated_content(client: OpenAI, messages, verbose: bool)-> None:
    for _ in range(MAX_ITERATIONS):

        response: ChatCompletion = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )

        if not response.usage:
            raise RuntimeError("API response appears to be malformed")

        message = response.choices[0].message
        messages.append(message)


        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose)
                messages.append(result_message)

                if not result_message["content"]:
                    raise Exception("Function call returned no content")
                if verbose :
                    print(f"Prompt tokens: {response.usage.prompt_tokens}")
                    print(f"Response tokens: {response.usage.completion_tokens}")
                    print(f"-> {result_message['content']}")

        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            break

    else:
        print("Max iterations reached without a final response")
        sys.exit(1)

if __name__ == "__main__":
    main()
