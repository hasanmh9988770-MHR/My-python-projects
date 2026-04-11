import logging
import requests
import sqlite3
import os
import torch
from datetime import datetime
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from groq import Groq
from dotenv import load_dotenv  # Added this

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

# ========= 1. LOAD CONFIGURATION =========
load_dotenv()  # This loads the variables from .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)

# ========= 2. LOGGING & DATABASE =========
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
conn = sqlite3.connect("bot_memory.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS history (user_id INTEGER, role TEXT, message TEXT)")
conn.commit()

# ========= 3. VISION MODEL (Pre-loaded) =========
print("⏳ Loading Vision Model... (Wait for 'JARVIS IS LIVE')")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=False)
vision_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# ... [Keep your get_weather, save_message, and get_memory functions here as they were] ...

# ========= 5. HANDLERS =========

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    raw_text = update.message.text
    text = raw_text.lower().strip()

    if "weather" in text:
        report = get_weather(text)
        await update.message.reply_text(report)
        return

    elif text in ["date", "today's date"]:
        await update.message.reply_text(f"📅 Today is {datetime.now().strftime('%A, %B %d, 2026')}")
        return
    elif text == "time":
        await update.message.reply_text(f"🕒 Current time: {datetime.now().strftime('%H:%M:%S')}")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        messages = [{"role": "system", "content": "You are Jarvis, a helpful AI. Keep responses short."}]
        messages += get_memory(user_id)
        messages.append({"role": "user", "content": raw_text})

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        reply = response.choices[0].message.content
        save_message(user_id, "user", raw_text)
        save_message(user_id, "assistant", reply)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ AI error: {str(e)}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("📸 Analyzing your image...")
    try:
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive("temp_vision.jpg")
        raw_image = Image.open("temp_vision.jpg").convert("RGB")
        inputs = processor(raw_image, return_tensors="pt")
        with torch.no_grad():
            out = vision_model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        await msg.edit_text(f"🧠 I see: {caption.capitalize()}.")
    except Exception as e:
        await msg.edit_text(f"⚠️ Vision error: {str(e)}")

# ========= 6. EXECUTION =========

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN not found in .env file!")
    else:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

        print("\n🔥 JARVIS IS LIVE")
        app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
