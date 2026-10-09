
import os
from dotenv import load_dotenv
from openai import OpenAI, APIStatusError, APIConnectionError

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise SystemExit(
        "ERROR: OPENROUTER_API_KEY is missing. "
        "Check your .env file."
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    timeout=60.0,
    max_retries=2,
)

print("Testing OpenRouter connection...")
print("Model: openrouter/free")

try:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": (
                    "Reply with exactly: "
                    "OpenRouter connection successful."
                ),
            }
        ],
        max_tokens=100,
    )

    choice = response.choices[0]
    content = choice.message.content

    print("\n========== TEST RESULT ==========")
    print("Model returned:", response.model)
    print("Finish reason:", choice.finish_reason)
    print("Response:", repr(content))
    print("Usage:", response.usage)

    if content and content.strip():
        print("\nSUCCESS: The model returned readable text.")
    else:
        print("\nWARNING: The model returned empty text.")

except APIStatusError as error:
    print("\nAPI ERROR")
    print("HTTP status:", error.status_code)
    print("Details:", error.message)

    if error.status_code == 429:
        print(
            "The free provider is rate-limited. "
            "Wait before retrying or select another available model."
        )
    elif error.status_code == 401:
        print("Check that your OpenRouter API key is valid.")
    elif error.status_code == 402:
        print("The request requires credits or paid access.")

except APIConnectionError as error:
    print("\nCONNECTION ERROR")
    print("Could not connect to OpenRouter:", error)

except Exception as error:
    print("\nUNEXPECTED ERROR")
    print(type(error).__name__, str(error))
