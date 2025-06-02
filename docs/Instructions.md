Jumble AI - Говорим про ИИ, [30.05.2025 11:52]
✨ Полный рабочий код бота с Gemini 2.5 Flash, который отвечает в чате на текст, голосовые и фото c полностью бесплатным API! #bot

Jumble AI - Говорим про ИИ, [30.05.2025 11:52]
📎 Ссылки и нужные команды:
✨ Google AI Studio (https://aistudio.google.com/prompts/new_chat)
🐍 Python 3.13 (https://www.python.org/downloads/)
➡️ Cursor AI (https://www.cursor.com/)

🚨 Доступ к Google AI Studio без VPN! (https://t.me/JumbleAI/53)

Модель которая используется в боте

gemini-2.5-flash-preview-05-20

Создание виртуального окружения python

python3 -m venv .venv

Активация виртуального окружения python
macOS/Linux
source .venv/bin/activate
Windows
source .venv\Scripts\activate

Зависимости python

pip install -U aiogram python-dotenv google-generativeai

Файл .env с Токенами и моделью

# .env

BOT*TOKEN="ВАШ*ТОКЕН"
GEMINI*API_KEY="ВАШ*КЛЮЧ"
MODEL_NAME="gemini-2.5-flash-preview-05-20"

Запустить бот

python bot.py

🧩 Jumble GPT (http://t.me/JumbleGPT_bot) | 📱 YouTube (https://www.youtube.com/results?search_query=%D0%92%D1%8F%D1%87%D0%B5%D1%81%D0%BB%D0%B0%D0%B2+%D0%9B%D1%8B%D0%BA%D0%BE%D0%B2)

Instructions

This document contains instructions for working with the project.

- To start the bot, run `python bot_geo_v1.py` after setting up the environment variables.
- Refer to README.md for setup and installation details.
- Memory bank files in the `memory-bank/` directory are used for collaborative work and understanding project context.
