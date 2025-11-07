import openai

client = openai.OpenAI(api_key="your-openai-apikey")

def ask_chatgpt(c):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": c}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "Sorry, I couldn't fetch a response right now."
