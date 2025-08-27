ECHO - Virtual Voice Assistant

Description:
Echo is a voice-activated virtual assistant that listens for a wake word ("Echo") and then responds to spoken commands.
It can switch languages, open websites, respond to greetings, and use AI to answer questions.

Features:
- Voice-activated (wake word: "Echo")
- Responds to basic prompts like "hello", "how are you", etc.
- Switches languages: English, Hindi, and French
- Opens common websites like Google, YouTube, LinkedIn, etc.
- Can respond using AI if API or simulated ChatGPT method is set up
- Uses both pyttsx3 (offline) and gTTS (online) for text-to-speech

How to Run:
1. First Install required packages:
   pip install -r requirements.txt
4. Run the main file:
   python main.py
5. afer ECHO is initialized, Say "Echo" or "hello" or "listen" and wait for echo to respond
6. after it responds, that means it is active.
7. Now say your command

Modules Required (see requirements.txt):
- SpeechRecognition
- pyttsx3
- gTTS
- playsound
- openai
- requests
- pyaudio

Notes:
- Make sure your microphone is working.
- For gTTS to work, internet connection is required.
- pyttsx3 works offline.