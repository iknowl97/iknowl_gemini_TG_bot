# Gemini Telegram Bot (Georgian Language v1.1)

This project is a Telegram bot developed in Python, designed to communicate in the Georgian language. It utilizes the Telegram Bot API to interact with users and is intended to be powered by a language model capable of generating literate and modern Georgian text.

## Features

- Responds to the `/start` command with a welcome message in Georgian.
- Provides information about the bot via the `/help` command in Georgian.
- Includes a basic handler for text messages (AI integration placeholder).
- Configured to use a system prompt in English optimized for generating high-quality Georgian output from an integrated AI model.

## Project Structure

```
GeminiTelegramBot/
├── .gitignore         # Specifies intentionally untracked files
├── bot.py             # Original bot implementation (reference)
├── bot_geo_v1.py      # Georgian language bot implementation (v1.1)
├── requirements.txt   # Project dependencies
├── README.md          # Project description and setup guide (this file)
├── memory-bank/       # Bot's memory and context storage
│   ├── activeContext.md
│   ├── featureMap.md
│   ├── georgian-prompts/ # Intended directory for Georgian prompts (currently not used for prompts)
│   ├── progress.md
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   └── techContext.md
└── .cursorrules       # Cursor's learned project patterns and intelligence
```

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd GeminiTelegramBot
    ```

2.  **Install dependencies:**

    Make sure you have Python installed. Then install the required libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Telegram Bot Token:**

    Obtain a bot token from the BotFather on Telegram. Set this token as an environment variable named `TELEGRAM_BOT_TOKEN`.

    - **On Windows:**

      ```bash
      $env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
      # Or permanently via System Properties > Environment Variables
      ```

    - **On macOS/Linux:**

      ```bash
      export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
      # Add to your shell profile (.bashrc, .zshrc, etc.) for permanence
      ```

4.  **Run the bot:**

    Execute the Python script:

    ```bash
    python bot_geo_v1.py
    ```

## AI Integration

Note that `bot_geo_v1.py` currently contains a placeholder for AI model integration. To make the bot functional beyond basic commands, you need to integrate a language model (like Gemini, GPT, etc.) capable of processing and generating Georgian text. Modify the `handle_message` function to call your chosen AI model's API.

The `SYSTEM_PROMPT_GEO` variable contains an English prompt designed to guide your AI model to produce high-quality, literate, and modern Georgian output. Ensure your AI integration utilizes this or a similar prompt effectively.

## Memory Bank

The `memory-bank/` directory contains documentation files used by the Cursor AI assistant to understand the project context, progress, and technical details. These files are not strictly necessary for running the bot but are crucial for collaborative development with Cursor.

## Contributing

Include instructions on how others can contribute to your project.

## License

Specify your project's license.
