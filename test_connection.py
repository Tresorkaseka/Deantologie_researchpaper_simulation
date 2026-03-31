"""Quick test of the configured LLM backend connection."""

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

from llm_backend import (
    create_llm_client,
    get_llm_api_key,
    get_llm_base_url,
    get_llm_model_name,
    get_llm_provider,
)


load_dotenv()

api_key = get_llm_api_key()
model_name = get_llm_model_name()
provider = get_llm_provider()
base_url = get_llm_base_url()

if not api_key:
    print("LLM_API_KEY was not found in .env")
    print("   -> Add your provider key to the environment file before running this check.")
    raise SystemExit(1)

print(f"Provider label: {provider}")
print(f"Model: {model_name}")
print("Testing the connection...")

try:
    client = create_llm_client(api_key=api_key, provider=provider, base_url=base_url)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are an ethical manager in a tech company.",
            },
            {
                "role": "user",
                "content": "In one sentence, how do you react to internal fraud?",
            },
        ],
        max_tokens=100,
        temperature=0.7,
    )
    print("\nConnection OK!")
    print(f"Answer: {response.choices[0].message.content.strip()}")
except Exception as exc:
    print(f"\nError: {exc}")
