import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def generate_test_code(prompt: str) -> str:
    """Generate test code for a given function.

    Args:
        prompt (str): The prompt containing the function code and context.

    Returns:
        str: The generated test code.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600,
    )
    return response.choices[0].message.content
