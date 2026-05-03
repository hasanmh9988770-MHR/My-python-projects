import pyttsx3
from PyDictionary import PyDictionary
import speech_recognition as spr
import platform

# Speaking class
class Speak:
    def SpeakWord(self, audio):
        # Select correct driver for platform
        system = platform.system()
        if system == 'Windows':
            driver = 'sapi5'
        elif system == 'Darwin':  # macOS
            driver = 'nsss'
        else:  # Linux
            driver = 'espeak'

        # Initialize pyttsx3 engine
        engine = pyttsx3.init(driver)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(audio)
        engine.runAndWait()

# Initialize recognizer and microphone
recognizer = spr.Recognizer()
mic = spr.Microphone()
speak = Speak()
dictionary = PyDictionary()

# Start the dictionary
with mic as source:
    print("Speak 'Hello' to initiate Speaking Dictionary!")
    speak.SpeakWord("Speak Hello to initiate Speaking Dictionary")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language='en-US').lower()
            if 'hello' in command:
                break
            else:
                print("Say 'Hello' to start.")
                speak.SpeakWord("Say Hello to start")
        except spr.UnknownValueError:
            print("Sorry, I did not catch that. Please try again.")
        except spr.RequestError as e:
            print(f"Google Speech API error: {e}")
            exit()

# Ask for the word
speak.SpeakWord("Which word do you want to find? Please speak slowly")
print("Which word do you want to find? Please speak slowly")

with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
    while True:
        try:
            audio = recognizer.listen(source)
            word = recognizer.recognize_google(audio, language='en-US').lower()
            break
        except spr.UnknownValueError:
            print("Sorry, I did not catch that. Please speak again.")
            speak.SpeakWord("Sorry, I did not catch that. Please speak again.")
        except spr.RequestError as e:
            print(f"Google Speech API error: {e}")
            exit()

# Fetch meaning and speak it
meaning = dictionary.meaning(word)
if meaning:
    print(f"Meaning of '{word}':")
    for part_of_speech, definitions in meaning.items():
        print(f"{part_of_speech}: {definitions}")
        speak.SpeakWord(f"{part_of_speech}: {', '.join(definitions)}")
else:
    print(f"Sorry, no meaning found for '{word}'.")
    speak.SpeakWord(f"Sorry, no meaning found for {word}")
