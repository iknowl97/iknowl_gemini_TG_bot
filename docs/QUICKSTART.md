# GeminiTelegramBot: სწრაფი დაწყება

ეს გზამკვლევი დაგეხმარებათ სწრაფად დაიწყოთ GeminiTelegramBot-ის მუშაობა.

1. **საცავის კლონირება:**
   გახსენით ტერმინალი და შეასრულეთ ბრძანებები:

   ```sh
   git clone <თქვენი-საცავის-მისამართი>
   cd GeminiTelegramBot
   ```

2. **დამოკიდებულებების ინსტალაცია Pipenv-ის გამოყენებით:**
   პროექტი იყენებს [Pipenv](https://pipenv.pypa.io/en/latest/) -ს დამოკიდებულებების სამართავად. თუ Pipenv არ გაქვთ დაინსტალირებული, დააინსტალირეთ გლობალურად ( დარწმუნდით, რომ არ ხართ ვირტუალურ გარემოში):

   ```sh
   pip install --user pipenv
   ```

   შემდეგ, პროექტის დირექტორიაში დააინსტალირეთ ყველა საჭირო ბიბლიოთეკა:

   ```sh
   pipenv install
   ```

   ეს შექმნის ვირტუალურ გარემოს და დააინსტალირებს `Pipfile`-ში მითითებულ ყველა დამოკიდებულებას.

3. **`.env` ფაილის კონფიგურაცია:**
   შექმენით `.env` ფაილი პროექტის ძირეულ დირექტორიაში შემდეგი შინაარსით. შეცვალეთ placeholder მნიშვნელობები თქვენი რეალური ტოკენებით და კლავიშებით.

   ```env
   BOT_TOKEN="თქვენი_TELEGRAM_BOT_TOKEN"
   GEMINI_API_KEY="თქვენი_GEMINI_API_KEY" # საჭიროა სურათის/აუდიოსთვის
   MODEL_NAME="gemini-2.5-flash-preview-05-20" # საჭიროა სურათის/აუდიოსთვის
   HUGGING_FACE_API_KEY="თქვენი_HUGGING_FACE_API_KEY" # საჭიროა ტექსტისთვის (RAG)
   HUGGING_FACE_MODEL="google/gemma-2b-it" # ნაგულისხმევი მოდელი ტექსტისთვის (RAG)
   ```

   - **`BOT_TOKEN`:** მიიღებთ [BotFather](https://core.telegram.org/bots#botfather)-გან Telegram-ში.
   - **`GEMINI_API_KEY`:** მიიღებთ [Google AI Studio](https://aistudio.google.com/)-დან (საჭიროა სურათების და ხმოვანი შეტყობინებების დამუშავებისთვის).
   - **`MODEL_NAME`:** Google Gemini მოდელის სახელი (მაგალითად, `gemini-2.5-flash-preview-05-20`).
   - **`HUGGING_FACE_API_KEY`:** მიიღებთ [Hugging Face](https://huggingface.co/settings/tokens)-დან (საჭიროა ტექსტური შეტყობინებებისთვის RAG-ით).
   - **`HUGGING_FACE_MODEL`:** Hugging Face მოდელის ID ტექსტის გენერაციისთვის (ნაგულისხმევად `google/gemma-2b-it`).

4. **ბოტის გაშვება:**
   გაუშვით ბოტი Pipenv ვირტუალურ გარემოში:

   ```sh
   pipenv run python bot_geo_v1.py
   ```

   ბოტი დაიწყებს მუშაობას და მზად იქნება შეტყობინებების მისაღებად Telegram-ში.

5. **საუბრის ისტორიის ჩატვირთვა (სურვილისამებრ):**
   თუ გაქვთ არსებული `user_conversations.csv` ფაილი და გსურთ მისი გამოყენება RAG-ისთვის ბოტის გაშვებამდე, დარწმუნდით, რომ ფაილი სწორ ადგილასაა (იმავე დირექტორიაში, სადაც `bot_geo_v1.py`). ბოტი ავტომატურად შეეცდება მის ჩატვირთვას გაშვებისას (თუ იყენებთ in-memory Chroma-ს, როგორც ამჟამად კონფიგურირებულია).
