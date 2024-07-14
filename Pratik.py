import openai
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
from datetime import datetime

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Set your OpenAI API key from environment variable
openai.api_key = 'API_key'

# Store the name of the creator
creator_name = "your_name"
creator_title = "Master"  # Can be "Sir" or "Master"

def record_audio(filename, duration=5, fs=44100):
    """Record audio from the microphone and save it to a file."""
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wav.write(filename, fs, recording)
    print("Recording complete")

def listen(filename="output.wav"):
    """Capture audio and convert it to text."""
    record_audio(filename)
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def get_response(prompt):
    """Get response from OpenAI GPT."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an Assistant named 'Pratik', who works and talks just like JARVIS. Your creator is {creator_name}, and you regard {creator_name} as your {creator_title} who created you using Python."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error getting response: {e}")
        return "I am sorry, I am unable to process your request at the moment, Master."

def open_website(site_name):
    """Open a specific website based on the site name."""
    urls = {
        "chrome": "https://www.google.com",
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.org",
        "instagram": "https://www.instagram.com",
        "gmail": "https://mail.google.com",
        "discord": "https://discord.com/app"
    }
    url = urls.get(site_name)
    if url:
        print(f"Opening {site_name.capitalize()}...")
        webbrowser.open(url)
        speak(f"Opening {site_name.capitalize()}, {creator_title}")
        return True
    else:
        return False

def get_time():
    """Get the current time."""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The current time is {current_time}, {creator_title}."

def main():
    print("AI Assistant is running...")

    while True:
        user_input = listen()
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Exiting...")
            break

        # Check if the user input contains any website command
        for site in ["chrome", "google", "youtube", "wikipedia", "instagram", "gmail", "discord"]:
            if site in user_input.lower():
                open_website(site)
                break
        else:
            # If no website command was found, process the input as a general prompt
            if user_input:
                if "time" in user_input.lower():
                    current_time = get_time()
                    print(f"AI: {current_time}")
                    speak(current_time)
                else:
                    response = get_response(user_input)
                    print(f"AI: {response}")
                    speak(response)

if __name__ == "__main__":
    main()
