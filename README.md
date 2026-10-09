# Assignment 2: Two-Bot AI Conversation CLI

A Python terminal application that runs a two-bot AI conversation through OpenRouter.

## Features

- User enters a topic or opening question in the terminal.
- Bot B starts first by default.
- Bot A and Bot B alternate for 3 complete exchanges.
- 3 complete exchanges means 6 generated replies:
  `Bot B -> Bot A -> Bot B -> Bot A -> Bot B -> Bot A`.
- Every model request includes the opening question and the full conversation history so each bot can respond to the discussion so far.
- Uses the OpenAI-compatible OpenRouter API with model `openrouter/free`.
- Reads `OPENROUTER_API_KEY` from environment variables.
- Handles missing API keys, rate limits, API errors, timeouts, connection failures, empty responses, and keyboard interrupts.

## Local Development

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file:

   ```text
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```

4. Optional: test the OpenRouter connection:

   ```powershell
   python test_groq.py
   ```

5. Run the conversation:

   ```powershell
   python main.py
   ```

6. Enter your own question when prompted.

## Files

- `main.py`: main two-bot conversation CLI.
- `test_groq.py`: quick OpenRouter connection test.
- `requirements.txt`: Python dependencies.
- `.env.example`: example environment variable file.

## Notes

- The script always uses `openrouter/free`.
- Do not hardcode or print your API key.
- The old frontend/Vercel version has been removed. This project is now terminal CLI based only.
