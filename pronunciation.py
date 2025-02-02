import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pygame import mixer
from datetime import date
import os

# Initialize mixer for audio playback
mixer.init()

# Set Google Gemini API key (replace 'Your-Google-API-key' or set as environment variable)
API_KEY = os.getenv("GEMINI_API_KEY", "Your-Google-API-key")
genai.configure(api_key=API_KEY)

# Define the model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()

gf = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 128,
}

safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Function to convert text to speech
def speak_text(text, lang='en'):
    mp3audio = BytesIO()
    tts = gTTS(text, lang=lang, tld='us')
    tts.write_to_fp(mp3audio)
    mp3audio.seek(0)
    mixer.music.load(mp3audio, "mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    mp3audio.close()

# Save conversation to log file
def append2log(text):
    fname = f'chatlog-{date.today()}.txt'
    with open(fname, "a", encoding='utf-8') as f:
        f.write(text + "\n")

# Main function
def main():
    try:
        rec = sr.Recognizer()
        mic = sr.Microphone()
        rec.dynamic_energy_threshold = False
        rec.energy_threshold = 400

        print("This program will check your pronunciation of a word.")
        word_to_pronounce = input("Enter the word you want to pronounce: ")
        
        request = f"You are a pronunciation evaluator. Listen to the user's pronunciation and determine if it is correct for the word '{word_to_pronounce}'. Respond with 'Correct pronunciation' or 'Incorrect pronunciation' and provide feedback."
        chat.send_message(request)
        
        while True:
            with mic as source:
                rec.adjust_for_ambient_noise(source, duration=0.5)
                print("Say the word...")
                audio = rec.listen(source, timeout=20, phrase_time_limit=5)
                try:
                    user_pronunciation = rec.recognize_google(audio, language='en')
                    if len(user_pronunciation) < 2:
                        continue
                    if "that's all" in user_pronunciation.lower():
                        append2log(f"You: {user_pronunciation}\n")
                        speak_text("Goodbye")
                        append2log("AI: Goodbye.\n")
                        print("Goodbye")
                        break
                    
                    eval_request = f"Did the user pronounce '{word_to_pronounce}' correctly? User said: '{user_pronunciation}'"
                    append2log(f"You: {eval_request}\n")
                    print(f"You: {user_pronunciation}\nAI:")
                    
                    response = chat.send_message(eval_request, generation_config=gf, safety_settings=safety_settings)
                    print(response.text)
                    speak_text(response.text.replace("*", ""))
                    append2log(f"AI: {response.text}\n")
                except Exception as e:
                    print(f"Error: {e}")
                    continue
    except AttributeError as e:
        print(f"Error: {e}")
        print("Please ensure PyAudio is installed correctly.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()