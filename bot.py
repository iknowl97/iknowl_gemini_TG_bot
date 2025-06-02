import asyncio
import logging
import os
import tempfile  # For temporary files
import pathlib   # For path operations

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Voice, PhotoSize
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# For Gemini API
import google.generativeai as genai
from google.generativeai.types import generation_types

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# Check for required tokens
if not BOT_TOKEN:
    raise ValueError("You must set the BOT_TOKEN environment variable.")
if not GEMINI_API_KEY:
    raise ValueError("You must set the GEMINI_API_KEY environment variable.")
if not MODEL_NAME:
    raise ValueError("You must set the MODEL_NAME environment variable.")

# System prompts
TEXT_SYSTEM_PROMPT = "You are a smart AI assistant in a Telegram chat. Reply concisely and clearly. Use emojis if appropriate."
AUDIO_SYSTEM_PROMPT = "You are a smart AI assistant. You have received a voice message. Please transcribe this audio and then reply concisely based on the transcribed text, as if the user wrote it. Use emojis if appropriate."
IMAGE_SYSTEM_PROMPT = "You are a smart AI assistant. You have received an image. Describe this image briefly, interestingly, and concisely, as if you were describing it to a friend. Use emojis if appropriate. 🖼️✨"
# ----------------------------------------------

# Gemini API setup
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use a model suitable for multimodal tasks (text + audio + images)
    gemini_model = genai.GenerativeModel(str(MODEL_NAME))
except Exception as e:
    logging.error(f"Gemini API configuration error: {e}")
    gemini_model = None

# Initialize router
router = Router()

# /start command handler


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_full_name = getattr(
        getattr(message, 'from_user', None), 'full_name', 'User')
    await message.answer(
        f"Hello, {user_full_name}!\n"
        "I'm your AI assistant. 🤖\n"
        "You can send me text, a voice message, or an image!"
    )

# /help command handler


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "This bot uses Gemini AI to generate responses.\n\n"
        "<b>Commands:</b>\n"
        "/start - Start a conversation\n"
        "/help - Show this message\n\n"
        "I can reply to text messages, process voice messages 🎤, and describe images 🖼️.\n"
        "I try to reply concisely and sometimes use emojis. 😉"
    )

# Text message handler


@router.message(F.text)
async def handle_text_message(message: Message):
    if not gemini_model:
        await message.answer("Sorry, the AI service is temporarily unavailable. Please try again later. 😔")
        return

    user_text = message.text
    if not user_text:
        await message.answer("Please enter some text. ✍️")
        return

    processing_message = await message.answer("Thinking... 🤔")

    try:
        prompt_with_instruction = f"{TEXT_SYSTEM_PROMPT}\n\nUser message: {user_text}"
        response = await gemini_model.generate_content_async(prompt_with_instruction)

        await processing_message.delete()

        if response.text:
            await message.answer(response.text)
        else:
            logging.warning(
                f"Gemini API returned an empty text response for: {user_text}")
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
            await message.answer(f"Unfortunately, I couldn't generate a response. 😔 Your request may have been too complex or violated the rules.{safety_feedback_info if safety_feedback_info else ''}")

    except generation_types.BlockedPromptException as bpe:
        logging.error(
            f"Text request to Gemini was blocked: {bpe} for text: {user_text}")
        await processing_message.delete()
        await message.answer("My internal filter found your text request unacceptable. 🙅‍♂️ Please try rephrasing.")
    except Exception as e:
        logging.error(
            f"Error when calling Gemini API (text): {e}", exc_info=True)
        try:
            await processing_message.delete()
        except Exception:
            pass
        await message.answer("Sorry, an error occurred while processing your text message. 😵‍💫")

# Voice message handler


@router.message(F.voice)
async def handle_voice_message(message: Message, bot: Bot):
    if not gemini_model:
        await message.answer("Sorry, the AI service is temporarily unavailable for audio processing. 😔")
        return

    voice = getattr(message, 'voice', None)  # type: ignore
    if voice is None:
        await message.answer("No voice message found in the request.")
        return
    processing_message = await message.answer("Processing your voice message... 🎤🎧")

    gemini_file_resource = None  # For proper Gemini file deletion

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir_path = pathlib.Path(temp_dir_name)
        local_ogg_path = temp_dir_path / f"{voice.file_unique_id}.ogg"

        try:
            logging.info(
                f"Downloading audio: {voice.file_id} to {local_ogg_path}")
            await bot.download(file=voice.file_id, destination=local_ogg_path)
            logging.info(
                f"Audio downloaded: {local_ogg_path}, size: {local_ogg_path.stat().st_size} bytes")

            if local_ogg_path.stat().st_size == 0:
                await processing_message.edit_text("Failed to download the audio file or the file is empty. 😥")
                return

            logging.info(f"Uploading {local_ogg_path} to Gemini Files API...")
            gemini_file_resource = await asyncio.to_thread(
                genai.upload_file,
                path=local_ogg_path,
                display_name=f"voice_message_{voice.file_unique_id}.ogg",
                mime_type="audio/ogg"
            )
            logging.info(
                f"Audio uploaded to Gemini: {gemini_file_resource.name}, URI: {gemini_file_resource.uri}")

            contents_for_gemini = [
                AUDIO_SYSTEM_PROMPT,
                gemini_file_resource
            ]

            response = await gemini_model.generate_content_async(contents_for_gemini)
            await processing_message.delete()

            if response.text:
                await message.answer(response.text)
            else:
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
                await message.answer(f"Unfortunately, I couldn't process your voice message. 🎤❌ It may have been unrecognized or violated the rules.{safety_feedback_info if safety_feedback_info else ''}")

        except generation_types.BlockedPromptException as bpe:
            logging.error(
                f"Gemini request for audio was blocked: {bpe} for file {voice.file_id}")
            await processing_message.delete()
            await message.answer("My internal filter found the audio or its request unacceptable. 🙅‍♂️ Please try another audio message.")
        except Exception as e:
            logging.error(
                f"Error processing voice message: {e}", exc_info=True)
            try:
                await processing_message.delete()
            except Exception:
                pass
            await message.answer("Sorry, an error occurred while processing your voice message. 😵‍💫 Please try again later.")
        finally:
            logging.info(
                f"Local file {local_ogg_path} (if created) will be deleted automatically.")
            if gemini_file_resource and hasattr(gemini_file_resource, 'name'):
                try:
                    logging.info(
                        f"Requesting deletion of file from Gemini: {gemini_file_resource.name}")
                    await asyncio.to_thread(genai.delete_file, name=gemini_file_resource.name)
                    logging.info(
                        f"File {gemini_file_resource.name} successfully deleted from Gemini.")
                except Exception as e_del:
                    logging.error(
                        f"Error deleting file from Gemini {gemini_file_resource.name}: {e_del}")

# Image message handler


@router.message(F.photo)
async def handle_photo_message(message: Message, bot: Bot):
    if not gemini_model:
        await message.answer("Sorry, the AI service is temporarily unavailable for image processing. 😔")
        return

    photos = getattr(message, 'photo', None)
    if not photos or not isinstance(photos, list):
        await message.answer("No image found in the request.")
        return
    photo: PhotoSize = photos[-1]
    processing_message = await message.answer("Analyzing the image... 🖼️👀")

    gemini_file_resource = None  # For proper Gemini file deletion

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir_path = pathlib.Path(temp_dir_name)
        # Telegram photos are usually JPEG
        local_jpg_path = temp_dir_path / f"{photo.file_unique_id}.jpg"

        try:
            logging.info(
                f"Downloading image: {photo.file_id} to {local_jpg_path}")
            await bot.download(file=photo.file_id, destination=local_jpg_path)
            logging.info(
                f"Image downloaded: {local_jpg_path}, size: {local_jpg_path.stat().st_size} bytes")

            if local_jpg_path.stat().st_size == 0:
                await processing_message.edit_text("Failed to download the image or the file is empty. 😥")
                return

            logging.info(f"Uploading {local_jpg_path} to Gemini Files API...")
            gemini_file_resource = await asyncio.to_thread(
                genai.upload_file,
                path=local_jpg_path,
                display_name=f"image_message_{photo.file_unique_id}.jpg",
                mime_type="image/jpeg"
            )
            logging.info(
                f"Image uploaded to Gemini: {gemini_file_resource.name}, URI: {gemini_file_resource.uri}")

            contents_for_gemini = [
                IMAGE_SYSTEM_PROMPT,
                gemini_file_resource
            ]

            response = await gemini_model.generate_content_async(contents_for_gemini)
            await processing_message.delete()

            if response.text:
                await message.answer(response.text)
            else:
                logging.warning(
                    f"Gemini API returned an empty response for image: {photo.file_id}")
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
                await message.answer(f"Unfortunately, I couldn't describe this image. 🖼️❌ It may have been unrecognized or violated the rules.{safety_feedback_info if safety_feedback_info else ''}")

        except generation_types.BlockedPromptException as bpe:
            logging.error(
                f"Gemini request for image was blocked: {bpe} for file {photo.file_id}")
            await processing_message.delete()
            await message.answer("My internal filter found the image or its request unacceptable. 🙅‍♂️ Please try another image.")
        except Exception as e:
            logging.error(f"Error processing image: {e}", exc_info=True)
            try:
                await processing_message.delete()
            except Exception:
                pass
            await message.answer("Sorry, an error occurred while processing your image. 😵‍💫 Please try again later.")
        finally:
            logging.info(
                f"Local file {local_jpg_path} (if created) will be deleted automatically.")
            if gemini_file_resource and hasattr(gemini_file_resource, 'name'):
                try:
                    logging.info(
                        f"Requesting deletion of file from Gemini: {gemini_file_resource.name}")
                    await asyncio.to_thread(genai.delete_file, name=gemini_file_resource.name)
                    logging.info(
                        f"File {gemini_file_resource.name} successfully deleted from Gemini.")
                except Exception as e_del:
                    logging.error(
                        f"Error deleting file from Gemini {gemini_file_resource.name}: {e_del}")


async def main():
    default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=str(BOT_TOKEN), default=default_properties)
    dp = Dispatcher()

    dp.include_router(router)

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
