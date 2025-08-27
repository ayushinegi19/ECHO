import webbrowser
import pywhatkit
from speech_utils import speak, set_language
from news import get_news
from gemini_ai import ask_gemini
from chatgpt import ask_chatgpt 
import datetime
from weather import get_weather
import difflib
from library import *
USE_GEMINI = True  # Change to False to use ChatGPT

# Flexible keyword detection
def contains(command, keywords):
    return any(kw in command for kw in keywords)

#-----------------------------------------------------------------------------------------------------------------------

def process_command(c):
    """Processes user voice commands"""
    c = c.lower().strip()
    print(f"User: {c}")

    if c in basic_responses:
        response = basic_responses[c]
        print(f"Echo: {response}")
        speak(response)
        return response

    elif "open" in c:
        site_name = c.replace("open", "").strip().lower()
        closest_match = difflib.get_close_matches(site_name, website_urls.keys(), n=1)

        if closest_match:
            url = website_urls[closest_match[0]]
            webbrowser.open(url)
            response = f"Opening {closest_match[0]}"
        else:
            response = f"Sorry, I don't recognize {site_name}"
        speak(response)
        return response

    elif "news" in c:
        get_news()
        return "Here are the latest news headlines."

    elif c.startswith("play "):
        play_music(c)
        return f"Searching and playing {c.replace('play', '').strip()}"

    elif contains(c, ["exit", "stop", "shut down", "quit", "goodbye", "bye"]):
        response = "Goodbye! Have a great day."
        speak(response)
        print("Exiting...")
        exit()

    elif contains(c, ["what's the date", "today's date", "tell me the date"]):
        response = datetime.datetime.now().strftime("Today is %A, %d %B %Y")
        speak(response)
        return response

    elif contains(c, ["what's the time", "tell me the time", "current time"]):
        response = datetime.datetime.now().strftime("The time is %I:%M %p")
        speak(response)
        return response

    elif "weather" in c:
        city = "Mumbai"
        if "in" in c:
            parts = c.split("in")
            if len(parts) > 1:
                city = parts[1].strip()

        response = get_weather(city)
        print(f"Echo: {response}")
        speak(response)
        return response

    elif contains(c, ["language to hindi", "switch to hindi"]):
        set_language("hi")
        response = "भाषा हिंदी में बदल दी गई है। आपकी सहायता के लिए मैं तैयार हूँ।"
        speak(response)
        return response

    elif contains(c, ["language to french", "switch to french"]):
        set_language("fr")
        response = "La langue a été changée en français. Je suis prêt à vous aider."
        speak(response)
        return response

    elif contains(c, ["language to english", "switch to english"]):
        set_language("en")
        response = "Language switched to English. I'm ready to assist you."
        speak(response)
        return response

    else:
        if USE_GEMINI:
            response = ask_gemini(c) + "\n(Powered by Gemini)"
        else:
            response = ask_chatgpt(c) + "\n(Powered by OpenAI)"
        speak(response)
        return response

            

#-----------------------------------------------------------------------------------------------------------------------

def play_music(command):
    song_name = command.replace("play", "").strip()
    speak(f"Searching YouTube for {song_name}")
    try:
        pywhatkit.playonyt(song_name)
        speak(f"Playing {song_name} on YouTube")
        print(f"Playing {song_name} on YouTube")
    except Exception as e:
        speak("Sorry, I had trouble playing the song.")
        print(f"Music Error: {e}")


