import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time
import os

# Initialize mixer for audio playback
mixer.init()

# Function to convert text to speech
def speak_text(text, lang='en'):
    try:
        mp3audio = BytesIO()
        tts = gTTS(text, lang=lang, tld='us')
        tts.write_to_fp(mp3audio)
        mp3audio.seek(0)

        # Save audio to a temporary file
        temp_filename = "temp_audio.mp3"
        with open(temp_filename, "wb") as f:
            f.write(mp3audio.read())

        mixer.music.load(temp_filename)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)

        os.remove(temp_filename)
    except Exception as e:
        print(f"Speech error: {e}")

# Function to check pronunciation
def check_pronunciation():
    rec = sr.Recognizer()
    mic = sr.Microphone()

    print("\nThis program will check your pronunciation of a word.")

    while True:
        word_to_pronounce = input("Enter the word you want to pronounce: ").strip()

        if not word_to_pronounce:
            print("No word entered. Exiting.")
            return

        print(f"\nPronounce the word: {word_to_pronounce}")
        speak_text(f"Please pronounce the word {word_to_pronounce}")

        with mic as source:
            rec.adjust_for_ambient_noise(source, duration=1.5)  # Noise reduction

            for attempt in range(3):  # Try up to 3 times
                print("\nSay the word...")

                try:
                    audio = rec.listen(source, timeout=5, phrase_time_limit=5)  # Longer listening time
                    user_pronunciation = rec.recognize_google(audio, language='en')

                    if user_pronunciation:
                        print(f"\nYou said: {user_pronunciation}")

                        if user_pronunciation.lower().strip() == word_to_pronounce.lower().strip():
                            feedback = "Correct pronunciation!"
                        else:
                            feedback = f"Incorrect pronunciation. You said '{user_pronunciation}', but it should be '{word_to_pronounce}'."

                        print(f"\nAI: {feedback}")
                        speak_text(feedback)
                        break  # Exit loop on success

                except sr.WaitTimeoutError:
                    print("\nNo speech detected. Please try again.")
                except sr.UnknownValueError:
                    print("\nSpeech not recognized. Try again.")
                except sr.RequestError:
                    print("\nCould not reach the speech recognition service. Check your internet connection.")

        retry = input("\nDo you want to try another word? (yes/no): ").strip().lower()
        if retry not in ['yes', 'y']:
            print("\nGoodbye!")
            speak_text("Goodbye")
            return  # Exit the function when the user stops

if __name__ == "__main__":
    check_pronunciation()
