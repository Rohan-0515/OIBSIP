import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess


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


# Google Search function
def google_search(query):
    search_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(search_url)
    speak("Here are the Google search results.")


def wikipedia_search(query):
    import wikipedia

    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)

    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")

    except wikipedia.exceptions.PageError:
        speak("Sorry, I could not find information about that topic.")

    except Exception:
        speak("Sorry, Wikipedia is currently unavailable.")


# Main program
if __name__ == "__main__":
    speak("Hello! I am your voice assistant. How can I help you?")

    while True:
        command = listen()

        if "hello" in command:
            speak("Hello! Nice to meet you.")

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {current_date}")

        elif "open youtube" in command:
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
        elif "who is" in command or "what is" in command:
            query = command.replace("who is", "").replace("what is", "").strip()

            if query:
                speak("Searching Wikipedia.")
                wikipedia_search(query)
            else:
                speak("Please tell me a topic.")
        elif "search" in command:
            query = command.replace("search", "").strip()

            if query:
                speak("Searching Google.")
                google_search(query)
            else:
                speak("Please tell me what you want to search.")

        elif "goodbye" in command or "exit" in command:
            speak("Goodbye! Have a nice day.")
            break

        elif command == "":
            continue

        else:
            speak("I am still learning. Please try another command.")
