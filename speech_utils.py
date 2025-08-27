import pyttsx3
from gtts import gTTS
from playsound import playsound
import tempfile
import os

# Initialize engines
engine = pyttsx3.init()
engine.setProperty('rate', 200) 
current_lang = 'en'
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # index 1 : female, Index 0: male


def speak(text):
    global current_lang

    if current_lang == 'en':
        # Use pyttsx3 for English (male voice, controlled speed)
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"pyttsx3 failed: {e}")
    else:
        # Use gTTS for non-English languages (natural voice)
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_filename = fp.name

            tts = gTTS(text=text, lang=current_lang)
            tts.save(temp_filename)
            playsound(temp_filename)

            os.unlink(temp_filename)
        except Exception as e:
            print(f"gTTS failed: {e}")

    

def set_language(lang_code):
    global current_lang
    current_lang = lang_code

    if lang_code == 'en':
        speak("Language switched to English. I'm ready to assist you.")
        print("Echo: Language switched to English. I'm ready to assist you.")
    elif lang_code == 'hi':
        speak("भाषा हिंदी में बदल दी गई है। आपकी सहायता के लिए मैं तैयार हूँ।")
        print("Echo: भाषा हिंदी में बदल दी गई है। आपकी सहायता के लिए मैं तैयार हूँ।")
    elif lang_code == 'fr':
        speak("La langue a été changée en français. Je suis prêt à vous aider.")
        print("Echo: La langue a été changée en français. Je suis prêt à vous aider.")
