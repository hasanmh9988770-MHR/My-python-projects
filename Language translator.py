from deep_translator import GoogleTranslator
from gtts import gTTS  # <--- ADDED
import os              # <--- ADDED

# Supported languages
language = {
    "bn": "Bangla", "en": "English", "ko": "Korean", "fr": "French", "de": "German",
    "he": "Hebrew", "hi": "Hindi", "it": "Italian", "ja": "Japanese", "la": "Latin",
    "ms": "Malay", "ne": "Nepali", "ru": "Russian", "ar": "Arabic", "zh-CN": "Chinese",
    "es": "Spanish"
}

# Language selection loop
allow = True
while allow:
    user_code = input("Input language code (or 'options'): ")
    if user_code.lower() == "options":
        for code, lang in language.items():
            print(f"{code} => {lang}")
    elif user_code in language:
        print(f"Selected: {language[user_code]}")
        allow = False
    else:
        print("Invalid code!")

# Translation loop
while True:
    string = input("\nText to translate (or 'close'): ")
    if string.lower() == "close":
        break

    try:
        # 1. Translate the text
        translator = GoogleTranslator(source='auto', target=user_code)
        translated_text = translator.translate(string)
        print(f"\n{language[user_code]}: {translated_text}")

        # 2. Create the audio file (ADDED)
        print("Playing audio...")
        tts = gTTS(text=translated_text, lang=user_code)
        tts.save("speech.mp3")

        # 3. Play the audio (MacOS command) (ADDED)
        os.system("afplay speech.mp3")

    except Exception as e:
        print(f"\nError: {e}")