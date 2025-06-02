import asyncio
import logging
import os
import tempfile  # For temporary files
import pathlib   # For path operations
import csv
from datetime import datetime

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Voice, PhotoSize, Document, Video, Audio, Sticker, Contact, Location
from aiogram.enums import ParseMode, ChatAction
from aiogram.client.default import DefaultBotProperties

# For Gemini API
import google.generativeai as genai
from google.generativeai.types import generation_types

# For RAG
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
HUGGING_FACE_MODEL = os.getenv("HUGGING_FACE_MODEL", "google/gemma-2b-it")

# Check for required tokens
if not BOT_TOKEN:
    raise ValueError("You must set the BOT_TOKEN environment variable.")
if not GEMINI_API_KEY:
    logging.warning(
        "GEMINI_API_KEY not set. Image/Audio/Document processing might be limited.")
if not MODEL_NAME:
    logging.warning(
        "MODEL_NAME not set. Image/Audio/Document processing might be limited.")
if not HUGGING_FACE_API_KEY:
    raise ValueError(
        "You must set the HUGGING_FACE_API_KEY environment variable for RAG.")

# Load system prompts from markdown files
PROMPT_DIR = pathlib.Path(__file__).parent / "prompts"


def load_prompt(filename):
    with open(PROMPT_DIR / filename, encoding="utf-8") as f:
        # skip the first line (title)
        return f.read().strip().split('\n', 1)[-1].strip()


TEXT_SYSTEM_PROMPT = load_prompt("text_system_prompt.md")
AUDIO_SYSTEM_PROMPT = load_prompt("audio_system_prompt.md")
IMAGE_SYSTEM_PROMPT = load_prompt("image_system_prompt.md")
# Load help and features text from markdown
HELP_TEXT = load_prompt("help_text.md")
FEATURES_TEXT = load_prompt("features_text.md")

# Gemini API setup
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(str(MODEL_NAME))
except Exception as e:
    logging.error(f"Gemini API configuration error: {e}")
    gemini_model = None

# RAG Setup
# Use a common embedding model
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

# Initialize Chroma with persistence (optional, removes need to re-embed each time)
# For simplicity, we'll use in-memory for now. Change to persistent later if needed.
# db_directory = "./chroma_db"
# vectorstore = Chroma(persist_directory=db_directory, embedding_function=embeddings)
vectorstore = Chroma(embedding_function=embeddings)

# Hugging Face LLM setup
hf_llm = HuggingFaceHub(
    repo_id=HUGGING_FACE_MODEL,
    task="text-generation",
    huggingfacehub_api_token=HUGGING_FACE_API_KEY,
)

# Create RetrievalQA chain (basic setup)
qa_chain = RetrievalQA.from_chain_type(
    llm=hf_llm,
    chain_type="stuff",  # Stuffing all retrieved documents into the prompt
    retriever=vectorstore.as_retriever()
)

router = Router()

# /start command handler


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_full_name = getattr(
        getattr(message, 'from_user', None), 'full_name', 'მომხმარებელი')
    await message.answer(
        f"გამარჯობა, {user_full_name}!\n"
        "მე ვარ შენი AI ასისტენტი. 🤖\n"
        "შეგიძლია გამომიგზავნო ტექსტი, ხმოვანი შეტყობინება ან სურათი!\n"
        "ყველა AI პასუხი იქნება თანამედროვე, გამართული ქართულით."
    )

# /help command handler


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT)
    log_conversation(message.from_user.id, getattr(
        message.from_user, 'username', ''), "/help", HELP_TEXT)

# Provide help/features info on user request (text/voice)
HELP_KEYWORDS = ["დახმარება", "help", "ფუნქცია",
                 "შესაძლებლობა", "features", "რას აკეთებ", "რა შეგიძლია"]


def is_help_request(text):
    return any(word in text.lower() for word in HELP_KEYWORDS)

# Helper to extract text from message (including caption, forwarded, etc.)


def extract_message_text(message: Message) -> str:
    parts = []
    if message.forward_from or message.forward_from_chat:
        parts.append("[Forwarded message]")
    if message.text:
        parts.append(message.text)
    if message.caption:
        parts.append(message.caption)
    return "\n".join(parts).strip()

# Generic handler for text, captions, and forwarded messages


@router.message(F.text | F.caption)
async def handle_text_and_caption_message(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    user_text = extract_message_text(message)

    # Check if the message is a help/features request
    if is_help_request(user_text):
        await message.answer(HELP_TEXT)
        log_conversation(message.from_user.id, getattr(
            message.from_user, 'username', ''), user_text, "Sent help text")
        return  # Stop processing if it's a help request

    if not gemini_model:
        await message.answer("უკაცრავად, AI სერვისი დროებით მიუწვდომელია. სცადეთ მოგვიანებით. 😔")
        log_conversation(message.from_user.id, getattr(
            message.from_user, 'username', ''), message.text, "AI სერვისი მიუწვდომელია")
        return

    if not user_text:
        await message.answer("გთხოვთ, შეიყვანეთ ტექსტი ან გამოგზავნეთ შეტყობინება აღწერით. ✍️")
        log_conversation(message.from_user.id, getattr(
            message.from_user, 'username', ''), user_text, "ტექსტი არ არის")
        return
    processing_message = await message.answer("ვაზროვნებ... ��")
    try:
        # Use RAG chain to get response
        # The qa_chain internally handles retrieval and generation
        response = await qa_chain.invoke({"query": user_text})

        await processing_message.delete()

        # The response from RetrievalQA is a dictionary, the answer is in the 'result' key
        if response and 'result' in response and response['result']:
            bot_response_text = response['result']
            await message.answer(bot_response_text)
            log_conversation(message.from_user.id, getattr(
                message.from_user, 'username', ''), user_text, bot_response_text)
        else:
            # Handle cases where RAG chain returns no result
            logging.warning(
                f"RAG chain returned no result for query: {user_text}")
            await message.answer("სამწუხაროდ, ვერ შევძელი თქვენს შეკითხვაზე პასუხის გაცემა კონტექსტის გამოყენებით. 😔")
            log_conversation(message.from_user.id, getattr(
                message.from_user, 'username', ''), user_text, "RAG chain returned no result")

    except Exception as e:
        await processing_message.delete()
        logging.error(f"Error in RAG chain processing: {e}", exc_info=True)
        await message.answer("უკაცრავად, შეტყობინების დამუშავებისას მოხდა შეცდომა. 😵‍💫")
        log_conversation(message.from_user.id, getattr(
            message.from_user, 'username', ''), user_text, "შეცდომა RAG დამუშავებისას")

# Enhanced image handler: supports photo and document with image MIME type


@router.message(F.photo | (F.document & (F.document.mime_type.startswith('image/'))))
async def handle_image_message(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    if not gemini_model:
        await message.answer("უკაცრავად, AI სერვისი დროებით მიუწვდომელია სურათებისთვის. 😔")
        log_conversation(message.from_user.id, getattr(
            message.from_user, 'username', ''), message.text, "AI სერვისი მიუწვდომელია")
        return
    # Get file info
    file_id = None
    file_unique_id = None
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_unique_id = photo.file_unique_id
        ext = 'jpg'
    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        ext = message.document.file_name.split(
            '.')[-1] if message.document.file_name else 'img'
    else:
        await message.answer("მოთხოვნაში სურათი ვერ მოიძებნა.")
        return
    processing_message = await message.answer("სურათის ანალიზი მიმდინარეობს... 🖼️👀")
    gemini_file_resource = None
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir_path = pathlib.Path(temp_dir_name)
        local_img_path = temp_dir_path / f"{file_unique_id}.{ext}"
        try:
            await bot.download(file=file_id, destination=local_img_path)
            if local_img_path.stat().st_size == 0:
                await processing_message.edit_text("Failed to download the image or the file is empty. 😥")
                log_conversation(message.from_user.id, getattr(
                    message.from_user, 'username', ''), message.text, "სურათი/ფაილი ცარიელია")
                return
            gemini_file_resource = await asyncio.to_thread(
                genai.upload_file,
                path=local_img_path,
                display_name=f"image_message_{file_unique_id}.{ext}",
                mime_type=f"image/{ext}" if ext in ['jpg', 'jpeg',
                                                    'png', 'gif', 'bmp', 'webp'] else 'image/jpeg'
            )
            # Combine caption if present
            caption = extract_message_text(message)
            contents_for_gemini = [IMAGE_SYSTEM_PROMPT]
            if caption:
                contents_for_gemini.append(f"Caption: {caption}")
            contents_for_gemini.append(gemini_file_resource)
            response = await gemini_model.generate_content_async(contents_for_gemini)
            await processing_message.delete()
            if response.text:
                await message.answer(response.text)
                log_conversation(message.from_user.id, getattr(
                    message.from_user, 'username', ''), message.text, response.text)
            else:
                # Handle cases where the main AI response is empty
                logging.warning(
                    f"Gemini API returned an empty response for image: {file_id}")
                safety_feedback_info = ""
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                    safety_feedback_info += f"\nReason (prompt_feedback): {response.prompt_feedback}"
                if hasattr(response, 'candidates') and response.candidates:
                    for i, candidate in enumerate(response.candidates):
                        if hasattr(candidate, 'finish_reason'):
                            safety_feedback_info += f"\nCandidate {i} (finish_reason): {candidate.finish_reason}"
                        if hasattr(candidate, 'safety_ratings'):
                            safety_feedback_info += f"\nCandidate {i} (safety_ratings): {candidate.safety_ratings}"
                logging.warning(safety_feedback_info)
                await message.answer(f"სამწუხაროდ, ვერ შევძელი სურათის აღწერა. 🖼️❌ მას შეიძლება მოხდეს, რომ შეტყობინება არ შეიძლება განმოწმებული ან წესებს შეერწყმა.{safety_feedback_info if safety_feedback_info else ''}")
                log_conversation(message.from_user.id, getattr(
                    message.from_user, 'username', ''), message.text, "სურათის აღწერა ვერ მოხერხდა")
        except Exception as e:
            await processing_message.delete()
            await message.answer("უკაცრავად, სურათის დამუშავებისას მოხდა შეცდომა. 😵‍💫")
            log_conversation(message.from_user.id, getattr(
                message.from_user, 'username', ''), message.text, "შეცდომა სურათის დამუშავებისას")
        finally:
            if gemini_file_resource and hasattr(gemini_file_resource, 'name'):
                try:
                    await asyncio.to_thread(genai.delete_file, name=gemini_file_resource.name)
                except Exception:
                    pass  # Silent failure on file deletion is acceptable

# Enhanced document/file handler (non-image)


@router.message(F.document & ~(F.document.mime_type.startswith('image/')))
async def handle_document_message(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    if not gemini_model:
        await message.answer("უკაცრავად, AI სერვისი დროებით მიუწვდომელია ფაილებისთვის. 😔")
        log_conversation(message.from_user.id, getattr(
            message.from_user, 'username', ''), message.text, "AI სერვისი მიუწვდომელია")
        return
    file_id = message.document.file_id
    file_unique_id = message.document.file_unique_id
    file_name = message.document.file_name or 'file'
    processing_message = await message.answer(f"მიმდინარეობს ფაილის '{file_name}' დამუშავება... 📄")
    gemini_file_resource = None
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir_path = pathlib.Path(temp_dir_name)
        local_file_path = temp_dir_path / file_name
        try:
            await bot.download(file=file_id, destination=local_file_path)
            if local_file_path.stat().st_size == 0:
                await processing_message.edit_text("Failed to download the file or the file is empty. 😥")
                log_conversation(message.from_user.id, getattr(
                    message.from_user, 'username', ''), message.text, "ფაილი ცარიელია")
                return
            gemini_file_resource = await asyncio.to_thread(
                genai.upload_file,
                path=local_file_path,
                display_name=file_name,
                mime_type=message.document.mime_type or 'application/octet-stream'
            )
            caption = extract_message_text(message)
            contents_for_gemini = [
                f"You have received a file. Analyze and summarize its content in modern, literate Georgian. If a caption is present, use it for context.",
            ]
            if caption:
                contents_for_gemini.append(f"Caption: {caption}")
            contents_for_gemini.append(gemini_file_resource)
            response = await gemini_model.generate_content_async(contents_for_gemini)
            await processing_message.delete()
            if response.text:
                await message.answer(response.text)
                log_conversation(message.from_user.id, getattr(
                    message.from_user, 'username', ''), message.text, response.text)
            else:
                await message.answer("სამწუხაროდ, ვერ შევძელი ფაილის დამუშავება. 📄❌")
        except Exception as e:
            await processing_message.delete()
            await message.answer("უკაცრავად, ფაილის დამუშავებისას მოხდა შეცდომა. 😵‍💫")
        finally:
            if gemini_file_resource and hasattr(gemini_file_resource, 'name'):
                try:
                    await asyncio.to_thread(genai.delete_file, name=gemini_file_resource.name)
                except Exception:
                    pass

# Voice message handler


@router.message(F.voice)
async def handle_voice_message(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    if not gemini_model:
        await message.answer("უკაცრავად, AI სერვისი დროებით მიუწვდომელია აუდიოსთვის. 😔")
        log_conversation(message.from_user.id, getattr(
            message.from_user, 'username', ''), message.text, "AI სერვისი მიუწვდომელია")
        return
    voice = getattr(message, 'voice', None)
    if voice is None:
        await message.answer("მოთხოვნაში ხმოვანი შეტყობინება ვერ მოიძებნა.")
        log_conversation(message.from_user.id, getattr(
            message.from_user, 'username', ''), message.text, "ხმოვანი შეტყობინება ვერ მოიძებნა")
        return
    processing_message = await message.answer("მიმდინარეობს თქვენი ხმოვანი შეტყობინების დამუშავება... 🎤🎧")
    gemini_file_resource = None
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir_path = pathlib.Path(temp_dir_name)
        local_ogg_path = temp_dir_path / f"{voice.file_unique_id}.ogg"
        try:
            await bot.download(file=voice.file_id, destination=local_ogg_path)
            if local_ogg_path.stat().st_size == 0:
                await processing_message.edit_text("აუდიო ფაილის ჩამოტვირთვა ვერ მოხერხდა ან ფაილი ცარიელია. 😥")
                log_conversation(message.from_user.id, getattr(
                    message.from_user, 'username', ''), message.text, "აუდიო ფაილი ცარიელია")
                return
            # Step 1: Transcribe the audio using Gemini
            gemini_file_resource = await asyncio.to_thread(
                genai.upload_file,
                path=local_ogg_path,
                display_name=f"voice_message_{voice.file_unique_id}.ogg",
                mime_type="audio/ogg"
            )
            # Step 2: Ask Gemini to transcribe only (Georgian, monospace)
            transcription_prompt = (
                "Transcribe this audio to modern, literate Georgian. "
                "Return only the transcription, no explanation."
            )
            transcription_response = await gemini_model.generate_content_async([
                transcription_prompt,
                gemini_file_resource
            ])
            transcription = (transcription_response.text or "").strip()
            # Step 3: Double-check/correct the transcription
            verify_prompt = (
                "Check the following Georgian transcription for accuracy and correct any errors. "
                "Return only the improved transcription, no explanation."
            )
            verify_response = await gemini_model.generate_content_async(
                f"{verify_prompt}\n\nTranscription: {transcription}"
            )
            verified_transcription = (
                verify_response.text or transcription).strip()
            # Step 4: Send the verified transcription to the user in monospace/code format
            if verified_transcription:
                await message.answer(f"<code>{verified_transcription}</code>", parse_mode="HTML")
            # Step 5: Generate the final AI reply as before
            contents_for_gemini = [AUDIO_SYSTEM_PROMPT, gemini_file_resource]
            response = await gemini_model.generate_content_async(contents_for_gemini)
            await processing_message.delete()
            if response.text:
                await message.answer(response.text)
                log_conversation(message.from_user.id, getattr(
                    message.from_user, 'username', ''), verified_transcription, response.text)
            else:
                # Handle cases where the main AI response is empty
                logging.warning(
                    f"Gemini API returned an empty response for audio: {voice.file_id}")
                safety_feedback_info = ""
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                    safety_feedback_info += f"\nReason (prompt_feedback): {response.prompt_feedback}"
                if hasattr(response, 'candidates') and response.candidates:
                    for i, candidate in enumerate(response.candidates):
                        if hasattr(candidate, 'finish_reason'):
                            safety_feedback_info += f"\nCandidate {i} (finish_reason): {candidate.finish_reason}"
                        if hasattr(candidate, 'safety_ratings'):
                            safety_feedback_info += f"\nCandidate {i} (safety_ratings): {candidate.safety_ratings}"
                logging.warning(safety_feedback_info)
                await message.answer(f"სამწუხაროდ, ვერ შევძელი თქვენი ხმოვანი შეტყობინების დამუშავება. 🎤❌ მას შეიძლება მოხდეს, რომ შეტყობინება არ შეიძლება განმოწმებული ან წესებს შეერწყმა.{safety_feedback_info if safety_feedback_info else ''}")
                log_conversation(message.from_user.id, getattr(message.from_user, 'username', ''), verified_transcription,
                                 f"პასუხი ვერ გენერირდა. სამწუხაროდ, ვერ შევძელი თქვენი ხმოვანი შეტყობინების დამუშავება. მას შეიძლება მოხდეს, რომ შეტყობინება არ შეიძლება განმოწმებული ან წესებს შეერწყმა.")
        except Exception as e:
            await processing_message.delete()
            await message.answer("უკაცრავად, ხმოვანი შეტყობინების დამუშავებისას მოხდა შეცდომა. 😵‍💫 სცადეთ მოგვიანებით.")
            log_conversation(message.from_user.id, getattr(
                message.from_user, 'username', ''), message.text, "შეცდომა ხმოვანი შეტყობინების დამუშავებისას")
        finally:
            if gemini_file_resource and hasattr(gemini_file_resource, 'name'):
                try:
                    await asyncio.to_thread(genai.delete_file, name=gemini_file_resource.name)
                except Exception:
                    pass  # Silent failure on file deletion is acceptable

# Video handler


@router.message(F.video)
async def handle_video_message(message: Message, bot: Bot):
    await message.answer("ვიდეო შეტყობინებების ანალიზი ჯერ არ არის მხარდაჭერილი, მაგრამ ეს ფუნქცია მალე დაემატება. 🎬")

# Audio handler


@router.message(F.audio)
async def handle_audio_message(message: Message, bot: Bot):
    await message.answer("აუდიო ფაილების ანალიზი ჯერ არ არის მხარდაჭერილი, მაგრამ ეს ფუნქცია მალე დაემატება. 🎵")

# Sticker handler


@router.message(F.sticker)
async def handle_sticker_message(message: Message):
    await message.answer("სტიკერები სახალისოა! 😄 თუმცა, სტიკერების ანალიზი ჯერ არ შემიძლია.")

# Contact handler


@router.message(F.contact)
async def handle_contact_message(message: Message):
    await message.answer("გამოგზავნილია კონტაქტი. კონტაქტების დამუშავება ჯერ არ შემიძლია, მაგრამ სხვა რამეზე თუ გჭირდებათ დახმარება, მომწერეთ!")

# Location handler


@router.message(F.location)
async def handle_location_message(message: Message):
    await message.answer("გამოგზავნილია ლოკაცია. ლოკაციების დამუშავება ჯერ არ შემიძლია, მაგრამ სხვა რამეზე თუ გჭირდებათ დახმარება, მომწერეთ!")

# Log conversation
LOG_FILE = pathlib.Path(__file__).parent / "user_conversations.csv"


def log_conversation(user_id, username, message, response):
    with open(LOG_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            user_id,
            username,
            message.replace("\n", " "),
            response.replace("\n", " ") if response else ""
        ])

# Function to load data from CSV and populate Chroma


def load_conversations_to_chroma(file_path: pathlib.Path):
    if not file_path.exists():
        logging.warning(
            f"Conversation log file not found at {file_path}. No data loaded to Chroma.")
        return
    try:
        # Using CSVLoader from Langchain
        loader = CSVLoader(file_path=str(file_path))
        documents = loader.load()

        if not documents:
            logging.info("No documents loaded from conversation log.")
            return

        # Add documents to Chroma
        # Note: This will re-add documents every time the bot starts if using in-memory Chroma.
        # For persistent Chroma, you'd check if the collection exists and is populated.
        vectorstore.add_documents(documents)
        logging.info(
            f"Loaded {len(documents)} documents into Chroma from {file_path}.")

    except Exception as e:
        logging.error(f"Error loading conversations to Chroma: {e}")


async def main():
    default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=str(BOT_TOKEN), default=default_properties)
    dp = Dispatcher()

    dp.include_router(router)

    # Load conversation data into Chroma on startup
    load_conversations_to_chroma(LOG_FILE)

    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("Bot is starting...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logging.info("Bot stopped.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    asyncio.run(main())
