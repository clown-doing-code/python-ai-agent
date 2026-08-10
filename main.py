import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import response

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ]
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")
    else:

        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print(f"Response: {response.choices[0].message.content}")

if __name__ == "__main__":
    main()
