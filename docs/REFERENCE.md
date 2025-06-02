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

- [Google AI Studio](https://aistudio.google.com/) ✨
- [Hugging Face](https://huggingface.co/) 🤗
- [Pipenv](https://pipenv.pypa.io/en/latest/) 📦
- [aiogram დოკუმენტაცია](https://docs.aiogram.dev/en/latest/) 📖
- [Langchain დოკუმენტაცია](https://python.langchain.com/v0.1/docs/) 📖
- [ChromaDB დოკუმენტაცია](https://docs.trychroma.com/) 📖
- [Sentence Transformers](https://www.sbert.net/) 📖
- [BotFather (Telegram)](https://core.telegram.org/bots#botfather) 🤖
