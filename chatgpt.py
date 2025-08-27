import openai

client = openai.OpenAI(api_key="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")

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
