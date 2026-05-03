import time
import os

# ========= MORSE DICTIONARY =========
symbols = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.",
    "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..",
    "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.",
    "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-",
    "y": "-.--", "z": "--..",
    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----"
}

# ========= TIMING =========
DOT_DURATION = 0.2
DASH_DURATION = 0.6
LETTER_GAP = 0.2
WORD_GAP = 0.6

# ========= SOUND =========
def beep(duration):
    os.system(f'play -n synth {duration} sine 1000')

# ========= PLAY MORSE =========
def play_morse(morse):
    for char in morse:
        if char == ".":
            beep(DOT_DURATION)
        elif char == "-":
            beep(DASH_DURATION)
        elif char == " ":
            time.sleep(LETTER_GAP)
        elif char == "/":
            time.sleep(WORD_GAP)

# ========= TRANSLATOR =========
def text_to_morse(text):
    text = text.lower()
    output = ""

    for char in text:
        if char in symbols:
            output += symbols[char] + " "
        elif char == " ":
            output += "/ "

    return output.strip()

# ========= MAIN =========
if __name__ == "__main__":
    print("🔥 MORSE GOD MODE ACTIVATED 🔥")

    while True:
        user_input = input("\nType text (or 'exit'): ")

        if user_input.lower() == "exit":
            print("👋 Exiting...")
            break

        morse = text_to_morse(user_input)

        print(f"\n📡 Morse Code:\n{morse}")

        print("\n🔊 Playing sound...")
        play_morse(morse)

    ## to run this in terminal: python "My Projects/Moss code translator.py"
    ## python 3.9