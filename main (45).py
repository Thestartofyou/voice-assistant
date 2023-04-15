import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# Initialize the speech recognizer and engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Set the voice assistant properties
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.7)

# Define the voice assistant commands
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except Exception as e:
            print("Sorry, I didn't catch that. Please try again.")
            return None

def open_website(url):
    webbrowser.open_new_tab(url)
    speak(f"Opening {url}")

def set_reminder():
    speak("What should I remind you about?")
    text = get_audio()
    if text:
        speak("When should I remind you?")
        text = get_audio()
        if text:
            try:
                date = datetime.datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.now()
                delta = (date - now).total_seconds()
                os.system(f'sleep {delta} && notify-send "Reminder" "{text}"')
                speak("Reminder set.")
            except ValueError:
                speak("Sorry, I didn't understand the time format.")

# Start the voice assistant
speak("Hi, I'm your voice assistant. How can I help you?")

while True:
    text = get_audio()
    if not text:
        continue
    if "hello" in text.lower():
        speak("Hi!")
    elif "open" in text.lower() and "website" in text.lower():
        words = text.split()
        for word in words:
            if word.startswith("http"):
                open_website(word)
                break
    elif "set" in text.lower() and "reminder" in text.lower():
        set_reminder()
    elif "exit" in text.lower() or "bye" in text.lower():
        speak("Goodbye!")
        break
