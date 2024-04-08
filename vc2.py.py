import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import pyjokes
import pytz
from gtts import gTTS
from datetime import datetime
import requests
LOCATIONS = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Mumbai": "Asia/Kolkata"
}

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
def listen():
    r = sr.Recognizer()

    # Validate that the user has a working microphone
    with sr.Microphone() as source:
        print("Speak something...")
        try:
            r.adjust_for_ambient_noise(source)
        except sr.WaitTimeoutError:
            print("Failed to calibrate microphone. Please check your microphone settings and try again.")
            return None

        print("Listening...")
        try:
            audio = r.listen(source)
        except sr.WaitTimeoutError:
            print("Timed out while listening. Please try again.")
            return None

        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return None

        return query.lower()
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
def assistant():
    while True:
        query = listen()
        if 'exit' in query:
            speak("Goodbye!")
            break
        elif "i love you" in query.lower():
            speak("I love you to")
        elif "tell me a joke" in query.lower():
            speak(tell_joke())
        elif 'who are you' in query or 'hu r u' in query or 'who r u' in query:
            speak("I am your assistant.")
        elif 'what is your name' in query:
            speak("I am rahi your assistant .")
        elif 'what is the time' in query:
            speak(f"The current time is {datetime.now().strftime('%I:%M %p')}")
        elif "time in" in query:
            location = query.replace("time in","").strip()
            if location in LOCATIONS:
                timezone = pytz.timezone(LOCATIONS[location])
                current_time = datetime.datetime.now(timezone)
                speak(f"The current time in {location} is {current_time.strftime('%H:%M')}.")
            else:
                speak(f"Sorry, I couldn't find the time in {location}.")    
        elif 'what is the date' in query:
            from datetime import date
            speak(f"Today's date is {date.today()}")
        elif "traffic in" in query:
            speak(f"the traffic is clear")    
        elif 'how are you' in query:
            speak("I am fine, thank you. How can I help you?")
        elif 'what\'s the weather like' in query or 'tell me the weather' in query:
            speak("I'm sorry, I cannot provide the weather information as I don't have access to the internet.")
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google.")
        elif 'play a song' in query:
            speak("Sure, what song would you like me to play?")
            query = listen()
            if 'cancel' not in query:
                try:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
                except Exception as e:
                    speak("Sorry, I couldn't find that song.")
        elif 'tell me a story' in query:
            speak("Once upon a time, in a land far, far away...")               
        elif 'search' in query:
            search_query = query.replace("search for", "")
            url = "https://www.google.com/search?q=" + search_query
            speak("Here are the results for your search:")
            webbrowser.open(url)
        elif 'stop listening' in query:
            print('Listening stopped')
            return False
    return True
speak("Hi, I am your assistant. How can I help you?")
speak("you can ask me to search for anything on the internet by saying 'search for' followed by your query")
listening = True
while listening:
    listening = assistant()
