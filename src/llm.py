import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not set in the .env file."
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    return client