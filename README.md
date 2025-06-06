# 🇬🇪✨ Telegram Bot: ქართული ვერსია (v1.1) ✨🇬🇪

👋 მოგესალმებით! ეს არის Telegram ბოტი, რომელიც სპეციალურად შეიქმნა ქართულ ენაზე კომუნიკაციისთვის. ის იყენებს Telegram Bot API-ს მომხმარებლებთან ურთიერთობისთვის და დაპროექტებულია ისე, რომ იმუშაოს ნებისმიერ ენის მოდელთან, რომელსაც შეუძლია გამართული, თანამედროვე ქართული ტექსტის გენერირება.

## 🚀 მახასიათებლები

- ✅ **`/start` ბრძანება:** გესალმებათ მისასალმებელი შეტყობინებით ქართულად.
- ❓ **`/help` ბრძანება:** გაწვდით ინფორმაციას ბოტის შესახებ ქართულ ენაზე.
- 💬 **ტექსტური შეტყობინებების დამუშავება:** მოიცავს ძირითად ფუნქციონალს ტექსტური შეტყობინებებისთვის (ენის მოდელის ინტეგრაციის ადგილი).
- ⚙️ **ოპტიმიზებული პრომპტები:** იყენებს ინგლისურ სისტემურ პრომპტს, რომელიც შემუშავებულია მაღალი ხარისხის ქართული პასუხების მისაღებად ინტეგრირებული ენის მოდელიდან.

## 📂 პროექტის სტრუქტურა

```
GeminiTelegramBot/
├── .gitignore         # იგნორირებული ფაილები
├── bot.py             # ძველი ბოტის კოდი (საცნობარო)
├── bot_geo_v1.py      # ქართული ბოტის კოდი (v1.1)
├── requirements.txt   # საჭირო ბიბლიოთეკები
├── README.md          # პროექტის აღწერა და ინსტრუქციები (ეს ფაილი)
├── memory-bank/       # ბოტის მეხსიერება და კონტექსტი
│   ├── activeContext.md
│   ├── featureMap.md
│   ├── georgian-prompts/ # პრომპტებისთვის განკუთვნილი საქაღალდე (ამჟამად არ გამოიყენება)
│   ├── progress.md
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   └── techContext.md
└── .cursorrules       # პროექტის თავისებურებები
```

## 🛠️ დაყენება და გაშვება

1.  **რეპოზიტორის კლონირება:**

    ```bash
    git clone <repository_url>
    cd GeminiTelegramBot
    ```

2.  **დამოკიდებულებების ინსტალაცია:**

    დარწმუნდით, რომ დაინსტალირებული გაქვთ Python. შემდეგ დააინსტალირეთ საჭირო ბიბლიოთეკები pip-ის გამოყენებით:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Telegram ბოტის ტოკენის დაყენება:**

    აიღეთ ბოტის ტოკენი BotFather-ისგან Telegram-ში. დააყენეთ ეს ტოკენი როგორც გარემოს ცვლადი (`environment variable`) სახელით `TELEGRAM_BOT_TOKEN`.

    - 🖥️ **Windows-ზე:**

      ```bash
      $env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
      # ან მუდმივად: System Properties > Environment Variables
      ```

    - 🍎🐧 **macOS/Linux-ზე:**

      ```bash
      export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
      # დაამატეთ თქვენს shell პროფილს (.bashrc, .zshrc, და ა.შ.) მუდმივობისთვის
      ```

4.  **ბოტის გაშვება:**

    გაუშვით Python სკრიპტი:

    ```bash
    python bot_geo_v1.py
    ```

## 🧠 ენის მოდელის ინტეგრაცია

გაითვალისწინეთ, რომ `bot_geo_v1.py` ამჟამად შეიცავს მხოლოდ ადგილს ენის მოდელის ინტეგრაციისთვის. იმისათვის, რომ ბოტმა იმუშაოს ძირითადი ბრძანებების მიღმა, საჭიროა ენის მოდელის (მაგ. Gemini, GPT, და ა.შ.) ინტეგრირება, რომელსაც შეუძლია ქართული ტექსტის დამუშავება და გენერირება. შეცვალეთ `handle_message` ფუნქცია, რათა გამოიძახოს თქვენი არჩეული ენის მოდელის API.

`SYSTEM_PROMPT_GEO` ცვლადი შეიცავს ინგლისურ პრომპტს, რომელიც შექმნილია თქვენი ენის მოდელის დასახმარებლად მაღალი ხარისხის, გამართული და თანამედროვე ქართული გამოსავლის მისაღებად. დარწმუნდით, რომ თქვენი ენის მოდელის ინტეგრაცია ეფექტურად იყენებს ამ ან მსგავს პრომპტს.

## 📖 Memory Bank (მეხსიერების ბანკი)

`memory-bank/` საქაღალდე შეიცავს დოკუმენტაციის ფაილებს, რომლებსაც იყენებს ასისტენტი პროექტის კონტექსტის, მიმდინარეობის და ტექნიკური დეტალების გასაგებად. ეს ფაილები აუცილებელი არ არის ბოტის გასაშვებად, მაგრამ მნიშვნელოვანია ქოლაბორაციული მუშაობისთვის.

## 🙌 როგორ შევიტანოთ წვლილი

აქ დაამატეთ ინსტრუქციები, თუ როგორ შეუძლიათ სხვებს წვლილის შეტანა თქვენს პროექტში.

## 📄 ლიცენზია

მიუთითეთ თქვენი პროექტის ლიცენზია.
