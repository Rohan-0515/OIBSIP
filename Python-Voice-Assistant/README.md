# Voice Assistant – Python Project

A Python-based Voice Assistant that uses speech recognition and text-to-speech to perform everyday tasks through voice commands.

This project was developed as part of the **Oasis Infobyte Python Programming Internship**.

## Features

### Beginner Version

- Voice recognition using microphone
- Text-to-speech responses
- Greeting messages
- Current date and time
- Google Search
- Open YouTube and Google
- Open Notepad and Calculator
- Wikipedia search
- Continuous listening
- Exit using voice commands

### Advanced Version

- All beginner features
- Send emails using Gmail SMTP
- Set timed reminders
- Get live weather information
- Search Wikipedia and answer general knowledge questions
- Natural Language Understanding (rule-based intent detection)
- Custom voice commands
- Voice-based interaction

## Technologies Used

- Python 3.12
- SpeechRecognition
- PyAudio
- pyttsx3
- Requests
- python-dotenv
- SMTP
- Open-Meteo API
- Wikipedia API
- Regular Expressions

## Project Structure

```text
Voice-Assistant/
│
├── Voice assistant.py
├── Voice assistant advance.py
├── README.md
├── Screenshorts/
├── .env
├── .gitignore
└── .venv/
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd Voice-Assistant
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install required packages

```bash
python -m pip install SpeechRecognition pyttsx3 PyAudio requests python-dotenv
```

## Email Configuration

The advanced version uses Gmail SMTP to send emails.

1. Enable 2-Step Verification in your Google Account.
2. Generate a Google App Password.
3. Create a `.env` file in the project folder.
4. Add the following configuration:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_google_app_password
```

**Important:** Never share your `.env` file or upload your email credentials to GitHub.

## How to Run

### Beginner Version

```bash
python "Voice assistant.py"
```

### Advanced Version

```bash
python "Voice assistant advance.py"
```

## Example Voice Commands

| Command                   | Action                   |
| ------------------------- | ------------------------ |
| Hello                     | Greeting                 |
| What is the time?         | Tells current time       |
| What is today's date?     | Tells current date       |
| Open YouTube              | Opens YouTube            |
| Open Google               | Opens Google             |
| Search Python programming | Google Search            |
| Who is Albert Einstein?   | Wikipedia answer         |
| What is today's weather?  | Weather information      |
| Send email                | Starts email process     |
| Remind me                 | Creates a timed reminder |
| Close / Exit              | Closes the assistant     |

## Weather API

Weather information is retrieved using the free Open-Meteo API.

Internet access is required for weather information and online searches.

## Privacy and Security

- Microphone access is required for voice recognition.
- Speech recognition uses Google's online recognition service.
- Email credentials are stored in a local `.env` file.
- The `.env` file must not be uploaded to GitHub.
- The `.venv` folder should also be excluded from version control.
- Internet connectivity is required for online features.

## Future Improvements

- Wake-word detection
- GUI interface
- More natural conversations
- Better NLP capabilities
- AI-powered question answering
- Additional system automation

## Author

**Python Programming Internship Project**

Developed using Python as part of the Oasis Infobyte Internship Program.

---

**Note:** This project is intended for educational and learning purposes.
