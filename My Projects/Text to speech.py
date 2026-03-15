from gtts import gTTS
import os

# --- Step 1: Secure the File Path ---
# This ensures Python looks in the SAME folder as this script for 'abc.txt'
base_dir = os.path.dirname(__file__)
text_file = os.path.join(base_dir, "abc.txt")
audio_file = os.path.join(base_dir, "voice.mp3")


def run_tts():
    try:
        # Step 2: Read the content
        with open(text_file, "r") as f:
            content = f.read().strip()

        if not content:
            print("⚠️ The file 'abc.txt' is empty! Please write something in it.")
            return

        print(f"🎙️  Converting text to speech...")

        # Step 3: Create the speech object
        # Note: Set lang='bn' if you want it to read Bengali text!
        speech = gTTS(text=content, lang='en', slow=False)

        # Step 4: Save the MP3
        speech.save(audio_file)
        print("✅ Audio file saved as 'voice.mp3'")

        # Step 5: Play it using Mac's native 'afplay'
        print("🔊 Playing audio now...")
        os.system(f"afplay '{audio_file}'")

    except FileNotFoundError:
        print(f"❌ Error: 'abc.txt' not found at: {text_file}")
        print("💡 Right-click your folder in PyCharm, select New > File, and name it 'abc.txt'.")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_tts()