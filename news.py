import requests
from speech_utils import speak

newsapi = "your-newsapi-key" 

def get_news():
    """ Fetches latest news headlines """
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            if articles:
                speak("Here are some latest news headlines.")
                for i, article in enumerate(articles[:5]):  # Limit to 5 headlines
                    print(f"News {i+1}: {article['title']}")
                    speak(f"News {i+1}: {article['title']}")
            else:
                speak("Sorry, I couldn't find any news at the moment.")
        else:
            speak("Error fetching news. Check your API key or internet connection.")
    except requests.exceptions.RequestException:
        speak("There was a problem connecting to the news service.")
