# GeminiTelegramBot Quickstart

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd GeminiTelegramBot
   ```
2. **Create and activate a virtual environment:**
   - macOS/Linux:
     ```sh
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows:
     ```sh
     python3 -m venv .venv
     .venv\Scripts\activate
     ```
3. **Install dependencies:**
   ```sh
   pip install -U -r requirements.txt
   ```
4. **Create a `.env` file:**
   ```env
   BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
   GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
   MODEL_NAME="gemini-2.5-flash-preview-05-20"
   ```
5. **Run the bot:**
   ```sh
   python bot.py
   ``` 