# GeminiTelegramBot: ცნობარი 📚

ეს დოკუმენტი შეიცავს ძირითად ცნობარ ინფორმაციას GeminiTelegramBot-ის შესახებ. ℹ️

## ბრძანებები ✨

- `/start` — იწყებს ახალ დიალოგს ბოტთან და აგზავნის მისასალმებელ შეტყობინებას. 👋
- `/help` — აჩვენებს დახმარების ტექსტს ბოტის შესაძლებლობებისა და გამოყენების შესახებ. ❓

## მხარდაჭერილი შეტყობინების ტიპები 📩

- **ტექსტური შეტყობინებები:** დამუშავდება Retrieval-Augmented Generation (RAG) მეთოდის გამოყენებით, კონტექსტის გათვალისწინებით საუბრების ისტორიიდან. 💬
- **ხმოვანი შეტყობინებები (OGG):** ტრანსკრიფცირდება ქართულად, გადამოწმდება და ანალიზდება Gemini API-ის გამოყენებით. 🎤
- **სურათები (ფოტო ან დოკუმენტი გამოსახულების MIME ტიპით):** ანალიზდება Gemini API-ის გამოყენებით და გენერირდება აღწერითი პასუხები. 🖼️
- **სხვა ტიპები (ვიდეო, აუდიო ფაილები, სტიკერები, კონტაქტები, ლოკაციები):** ამჟამად არ არის სრულად მხარდაჭერილი. ბოტი გამოგიგზავნით შეტყობინებას, რომ ვერ ამუშავებს ამ ტიპის კონტენტს. ❌

## გარემოს ცვლადები (`.env` ფაილი) ⚙️

- `BOT_TOKEN` — თქვენი Telegram Bot API ტოკენი, რომელიც მიიღეთ BotFather-ისგან. 🔑
- `GEMINI_API_KEY` — თქვენი Google Gemini API კლავიში (საჭიროა სურათების და ხმოვანი შეტყობინებების დამუშავებისთვის). ✨
- `MODEL_NAME` — Google Gemini მოდელის სახელი, რომელიც გამოყენებული იქნება (მაგალითად, `gemini-2.5-flash-preview-05-20`). 🧠
- `HUGGING_FACE_API_KEY` — თქვენი Hugging Face API კლავიში (საჭიროა ტექსტური შეტყობინებებისთვის RAG-ით). 🤗
- `HUGGING_FACE_MODEL` — Hugging Face ტექსტის გენერაციის მოდელის ID, რომელიც გამოყენებული იქნება RAG-ისთვის (ნაგულისხმევად `google/gemma-2b-it`). 🤖

## დამოკიდებულებები 📦

პროექტი იყენებს [Pipenv](https://pipenv.pypa.io/en/latest/)-ს დამოკიდებულებების სამართავად. ყველა საჭირო ბიბლიოთეკა ჩამოთვლილია `Pipfile`-ში, მათ შორის:

- `aiogram` — Telegram Bot API-თან ურთიერთობისთვის. 📱
- `python-dotenv` — `.env` ფაილიდან გარემოს ცვლადების ჩასატვირთად. 📄
- `google-generativeai` — Google Gemini API-სთან მუშაობისთვის. ✨
- `langchain` — RAG პროცესის ორკესტრირებისთვის. 🔗
- `chromadb` — ვექტორული მონაცემთა ბაზისთვის. 🗄️
- `transformers` — Hugging Face მოდელებთან მუშაობისთვის. 🤗
- `sentence-transformers` — ტექსტის ვექტორული წარმოდგენების (embeddings) გენერირებისთვის. 📊

## ფაილები და დირექტორიები 📁

- `bot_geo_v1.py` — ბოტის ძირითადი კოდი. 🐍
- `README.md` — პროექტის აღწერა (ქართულად). 📖🇬🇪
- `.env` — გარემოს ცვლადების კონფიგურაცია. 🔑
- `Pipfile` / `Pipfile.lock` — Pipenv დამოკიდებულებების მართვის ფაილები. 🔒
- `user_conversations.csv` — მომხმარებელთა საუბრების ისტორია. 💾
- `prompts/` — დირექტორია AI პრომპტების და სტატიკური ტექსტებისთვის (.md ფაილები). ✍️
- `docs/` — დამატებითი დოკუმენტაცია (ყველა ქართულად). 📚

## სასარგებლო ბმულები 👇

- [Google AI Studio](https://aistudio.google.com/) (წვდომა VPN-ის გარეშე: https://t.me/JumbleAI/53) ✨
- [Hugging Face](https://huggingface.co/) 🤗
- [Pipenv](https://pipenv.pypa.io/en/latest/) 📦
- [aiogram დოკუმენტაცია](https://docs.aiogram.dev/en/latest/) 📖
- [Langchain დოკუმენტაცია](https://python.langchain.com/v0.1/docs/) 📖
- [ChromaDB დოკუმენტაცია](https://docs.trychroma.com/) 📖
- [Sentence Transformers](https://www.sbert.net/) 📖
- [BotFather (Telegram)](https://core.telegram.org/bots#botfather) 🤖
- [Python 3.13+](https://www.python.org/downloads/) 🐍

# REFERENCES

This document provides a list of references and resources used in the Gemini Telegram Bot project.

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api) ➡️ Essential guide for interacting with the Telegram Bot API.
- [python-telegram-bot Library](https://python-telegram-bot.readthedocs.io/en/stable/) ➡️ The Python library used to simplify interaction with the Telegram Bot API.
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) ➡️ Library for various natural language processing tasks, including embeddings and models for RAG.
- [LangChain](https://python.langchain.com/docs/get_started/introduction) ➡️ Framework for developing applications powered by language models.
- [Chroma](https://www.trychroma.com/) ➡️ Open-source embeddings database used for RAG.
- [dotenv](https://github.com/theskumar/python-dotenv) ➡️ For loading environment variables from a .env file.
