import requests

def get_weather(city):
    api_key = "39fbf873455724afb6e0f64b935058c5"  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        res = requests.get(url)
        data = res.json()

        if data.get("cod") != 200:
            return f"Sorry, I couldn't fetch the weather for {city}."

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        return f"Currently in {city}, it's {weather}, with a temperature of {temp}°C, feels like {feels_like}°C."

    except Exception as e:
        print("Weather API Error:", e)
        return "Sorry, weather information is not available right now."
