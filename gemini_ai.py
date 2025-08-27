import google.generativeai as genai
import os

API_KEY = "AIzaSyCxOC0jF3MZj4rwcv5EIjFDmPIFyvk0rY8"
genai.configure(api_key=API_KEY)

def ask_gemini(c):
    try:
        # Use a model available in the free tier
        model = genai.GenerativeModel('gemini-1.5-flash')

        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 150,
        }

        response = model.generate_content(
            c,
            generation_config=generation_config
        )

        if hasattr(response, 'text') and response.text:
            return response.text
        else:
            return "I received an empty response. Please try asking something else."

    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Sorry, I couldn't fetch a response from Gemini right now."
