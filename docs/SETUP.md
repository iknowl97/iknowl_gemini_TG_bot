# GeminiTelegramBot Setup Guide

## Prerequisites
- Python 3.13+ ([Download Python](https://www.python.org/downloads/))
- Telegram account and bot token ([BotFather](https://core.telegram.org/bots#botfather))
- Gemini API key ([Google AI Studio](https://aistudio.google.com/prompts/new_chat))

## 1. Clone the Repository
```sh
git clone <your-repo-url>
cd GeminiTelegramBot
```

## 2. Create a Virtual Environment
```sh
python3 -m venv .venv
```

### Activate the Virtual Environment
- **macOS/Linux:**
  ```sh
  source .venv/bin/activate
  ```
- **Windows:**
  ```sh
  .venv\Scripts\activate
  ```

## 3. Install Dependencies
```sh
pip install -U -r requirements.txt
```

## 4. Configure Environment Variables
Create a `.env` file in the project root with the following content:

```env
BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
MODEL_NAME="gemini-2.5-flash-preview-05-20"
```

## 5. Run the Bot
```sh
python bot.py
```

## Useful Links
- [Google AI Studio](https://aistudio.google.com/prompts/new_chat)
- [Cursor AI](https://www.cursor.com/)
- [Jumble GPT Telegram Bot](http://t.me/JumbleGPT_bot) 