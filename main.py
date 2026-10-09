
import os
import sys
from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/free"
EXCHANGES = 3
TOTAL_REPLIES = EXCHANGES * 2
MAX_TOKENS = 400

if not API_KEY:
    raise SystemExit("ERROR: OPENROUTER_API_KEY is missing from .env")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=60.0,
    max_retries=2,
)

BOT_PROMPTS = {
    "Bot A": (
        "You are Bot A, an optimistic technology enthusiast. "
        "Give thoughtful, concise responses. Engage directly with "
        "the other bot's arguments and develop the discussion. "
        "Keep your response under 160 words."
    ),
    "Bot B": (
        "You are Bot B, a critical thinker. "
        "Question assumptions, provide counterarguments, and "
        "respond directly to the other bot. "
        "Keep your response under 160 words."
    ),
}

TURN_ORDER = ["Bot B", "Bot A"] * EXCHANGES


def get_reply(system_prompt, conversation):
    """Generate one response using the shared conversation history."""
    messages = [
        {"role": "system", "content": system_prompt},
        *conversation,
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=0.7,
    )

    reply = response.choices[0].message.content

    if not reply or not reply.strip():
        raise RuntimeError("The model returned an empty response.")

    return reply.strip()


def explain_api_error(error):
    """Return a readable message for common OpenRouter failures."""
    if isinstance(error, APIStatusError):
        if error.status_code == 429:
            return (
                "OpenRouter is rate-limited right now. "
                "Wait a little and run the script again."
            )
        if error.status_code in (401, 403):
            return "OpenRouter rejected the API key. Check OPENROUTER_API_KEY in .env."
        if error.status_code == 402:
            return "OpenRouter requires credits or provider access for this request."

        return f"OpenRouter returned HTTP {error.status_code}: {error.message}"

    if isinstance(error, APITimeoutError):
        return "OpenRouter timed out before returning a response."

    if isinstance(error, APIConnectionError):
        return f"Could not connect to OpenRouter: {error}"

    return f"{type(error).__name__}: {error}"


def main():
    user_question = input("Enter your topic or opening question: ").strip()

    if not user_question:
        raise SystemExit("ERROR: Please enter a question before starting.")

    conversation = [
        {"role": "user", "content": f"Opening question/topic: {user_question}"}
    ]

    print("\n========== TWO-BOT CONVERSATION ==========")
    print(f"Opening question: {user_question}")
    print(f"Model router: {MODEL}")
    print(f"Complete exchanges planned: {EXCHANGES}")
    print(f"Bot replies planned: {TOTAL_REPLIES}")
    print("Starting speaker: Bot B")

    try:
        for turn, bot_name in enumerate(TURN_ORDER, start=1):
            system_prompt = BOT_PROMPTS[bot_name]

            print(f"\n[{turn}/{TOTAL_REPLIES}] {bot_name} is thinking...")

            reply = get_reply(system_prompt, conversation)

            print(f"\n{bot_name}:")
            print(reply)

            # Add each response so the next bot sees the discussion.
            conversation.append({
                "role": "assistant",
                "content": f"{bot_name}: {reply}",
            })

    except KeyboardInterrupt:
        print("\nConversation interrupted by user.")
        sys.exit(1)

    except Exception as error:
        print(f"\nConversation failed: {explain_api_error(error)}")
        sys.exit(1)

    print("\n========== CONVERSATION COMPLETE ==========")
    print(f"Complete exchanges generated: {EXCHANGES}")
    print(f"Bot replies generated: {TOTAL_REPLIES}")


if __name__ == "__main__":
    main()
