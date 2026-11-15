import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import time
import requests
import re

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Speak function
def speak(text):
    print("Assistant:", text)

    try:
        engine = pyttsx3.init("sapi5")
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Voice Error:", e)


# Listen function
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Please repeat.")
        return ""

    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""


def listen_for_number():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for number...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

    try:
        number = recognizer.recognize_google(audio)
        print("Detected number:", number)
        return number.lower()

    except sr.UnknownValueError:
        speak("I could not understand the number.")
        return ""

    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

    except sr.WaitTimeoutError:
        speak("No input detected.")
        return ""


# get weather
def get_weather(city):

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}

        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            speak("Sorry, city not found.")
            return

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code",
            "timezone": "auto",
        }

        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        weather_data = weather_response.json()

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        feels_like = current["apparent_temperature"]
        weather_code = current["weather_code"]

        if weather_code == 0:
            condition = "Clear sky"
        elif weather_code in [1, 2, 3]:
            condition = "Partly cloudy"
        elif weather_code in [45, 48]:
            condition = "Foggy"
        elif weather_code in [51, 53, 55, 56, 57]:
            condition = "Drizzling"
        elif weather_code in [61, 63, 65, 66, 67]:
            condition = "Rainy"
        elif weather_code in [71, 73, 75, 77]:
            condition = "Snowy"
        elif weather_code in [80, 81, 82]:
            condition = "Rain showers"
        elif weather_code in [85, 86]:
            condition = "Snow showers"
        elif weather_code in [95, 96, 99]:
            condition = "Thunderstorm"
        else:
            condition = "Unknown"

        print(f"Weather in {city_name}")
        print(f"Condition: {condition}")
        print(f"Temperature: {temperature}°C")
        print(f"Feels like: {feels_like}°C")
        print(f"Humidity: {humidity}%")
        speak(f"The weather condition in {city_name} is {condition}.")
        speak(f"The temperature in {city_name} is {temperature} degrees Celsius.")
        speak(f"Feels like {feels_like} degrees.")
        speak(f"Humidity is {humidity} percent.")

    except requests.RequestException as e:
        print("Weather API Error:", e)
        speak("Unable to fetch weather information.")

    except (KeyError, ValueError) as e:
        print("Weather Data Error:", e)
        speak("Weather information is unavailable.")


# Google Search function
def google_search(query):
    search_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(search_url)
    speak("Here are the Google search results.")


# Wikipedia search
def wikipedia_search(query):

    try:
        headers = {"User-Agent": "VoiceAssistant/1.0 (student project)"}

        search_url = "https://en.wikipedia.org/w/api.php"

        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
        }

        search_response = requests.get(
            search_url, params=search_params, headers=headers, timeout=10
        )

        search_response.raise_for_status()
        search_data = search_response.json()

        results = search_data["query"]["search"]

        if not results:
            speak("Sorry, I could not find that topic.")
            return

        page_title = results[0]["title"]

        summary_url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + requests.utils.quote(page_title, safe="")
        )

        summary_response = requests.get(summary_url, headers=headers, timeout=10)

        summary_response.raise_for_status()
        summary_data = summary_response.json()

        summary = summary_data.get("extract", "")

        if summary:
            speak(summary[:700])
        else:
            speak("Sorry, no summary found.")

    except requests.RequestException as e:
        print("Wikipedia API Error:", e)
        speak("Wikipedia service is unavailable.")

    except (ValueError, KeyError) as e:
        print("Wikipedia Data Error:", e)
        speak("Sorry, I could not process the information.")


# send email
def send_email(receiver, subject, message):

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        speak("Email credentials are missing.")
        return

    try:
        email = EmailMessage()
        email["From"] = EMAIL_ADDRESS
        email["To"] = receiver
        email["Subject"] = subject
        email.set_content(message)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(email)

        speak("Email sent successfully!")

    except Exception as e:
        print("Email Error:", e)
        speak("Sorry, I could not send the email.")


# Reminder
def set_reminder(seconds, reminder_message):
    print("Reminder started...")
    speak(f"Reminder set for {seconds} seconds.")

    time.sleep(seconds)

    print("Reminder triggered!")
    speak(f"Reminder! {reminder_message}")


# Natural Language Understanding (NLP)
def understand_command(command):

    command = command.lower()
    command = re.sub(r"[^\w\s]", "", command)

    if any(word in command for word in ["time", "clock"]):
        return "time"

    elif any(word in command for word in ["weather", "temperature", "forecast"]):
        return "weather"

    elif any(word in command for word in ["date", "today", "day"]):
        return "date"

    elif any(word in command for word in ["youtube", "play video"]):
        return "youtube"

    elif any(word in command for word in ["google", "search", "find"]):
        return "search"

    elif any(word in command for word in ["email", "send mail"]):
        return "email"

    elif any(word in command for word in ["remind", "reminder"]):
        return "reminder"

    elif any(word in command for word in ["wikipedia", "who is", "what is"]):
        return "wikipedia"

    elif any(word in command for word in ["close", "stop", "exit", "goodbye"]):
        return "exit"

    else:
        return "unknown"


# Main program
if __name__ == "__main__":
    speak("Hello! I am your voice assistant. How can I help you?")

    while True:
        command = listen()

        intent = understand_command(command)
        print("Detected Intent:", intent)

        if "hello" in command:
            speak("Hello! Nice to meet you.")

        if intent == "time":
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif intent == "date":
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {current_date}")

        elif intent == "youtube":
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "open notepad" in command:
            speak("Opening Notepad.")
            subprocess.Popen(["notepad.exe"])

        elif "open calculator" in command:
            speak("Opening Calculator.")
            subprocess.Popen(["calc.exe"])

        elif intent == "wikipedia":
            query = command.replace("who is", "").replace("what is", "").strip()

            if query:
                speak("Searching Wikipedia.")
                wikipedia_search(query)
            else:
                speak("Please tell me a topic.")

        elif intent == "email":
            speak("Please tell me the receiver email address.")
            receiver = listen()
            receiver = receiver.replace(" at ", "@").replace(" dot ", ".")
            receiver = receiver.replace(" ", "")

            speak("Please tell me the email subject.")
            subject = listen()

            speak("Please tell me your message.")
            message = listen()

            speak(f"Your email subject is {subject}.")
            speak("Do you want to send this email? Say ha or na.")
            confirmation = listen()
            confirmation = (
                confirmation.strip().lower().replace(".", "").replace("!", "")
            )

            if confirmation.strip().lower() in [
                "yes",
                "yeah",
                "yep",
                "haan",
                "ha",
                "han",
            ]:
                send_email(receiver, subject, message)

            else:
                speak("Email sending cancelled.")

        elif intent == "reminder":
            speak("What should I remind you about?")
            reminder_message = listen()

            speak("After how many seconds?")
            speak("Please type the reminder time in seconds.")

            reminder_time = input("Enter seconds: ").strip()

            try:
                seconds = int(reminder_time)

                if seconds <= 0:
                    speak("Please enter a positive number.")
                else:
                    set_reminder(seconds, reminder_message)

            except ValueError:
                speak("Please enter a valid number.")

        elif intent == "weather":
            speak("Please tell me the city name.")
            city = input("Enter city name: ").strip()

            if city:
                get_weather(city)

        elif intent == "search":
            query = command.replace("search", "").strip()

            if query:
                speak("Searching Google.")
                google_search(query)
            else:
                speak("Please tell me what you want to search.")

        elif intent == "exit":
            speak("Goodbye! Have a nice day.")
            break

        elif command == "":
            continue

        else:
            speak("I am still learning. Please try another command.")
