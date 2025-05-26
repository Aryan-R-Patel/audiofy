# Audiofy - PDF to MP3 Converter    

**Audiofy** is a web application that converts PDF files to MP3 audio files, making it easier for users to listen to their documents on the go.

---

## How it works
- 📁 Upload a PDF file (or paste text)
- 🎧 Convert text content to MP3 using gTTS (Google Text-To-Speech API)
- 🤖 Generates an AI-based summary of the uploaded text using Gemini API

---

## Tech Stack
- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Python, Flask
- **Database**: SQLite
- **Libraries**: gTTS, PyPDF2, Gemini API

---

## Installation (Run Locally)
Open a terminal and navigate to the directory where you want to install the project:
```bash
# Clone the repository
git clone https://github.com/Aryan-R-Patel/audiofy.git

# Change to the app directory
cd audiofy

# Install the required libraries/packages
pip install -r requirements.txt

# ⚠ NOTE: Please complete the steps listed in the "Environment Variables" section before proceeding

# Run the application
flask run
```
Then open http://localhost:5000 in your browser to view your app!

---

## Environment Variables
Before running the app, create a .env file in the root directory and add the following:
```env
GEMINI_API_KEY = "your-secret-key-here"
PROMPT = "your-prompt-here"
```
Replace "*your-secret-key-here*" with your GEMINI_API_KEY and "*your-prompt-here*"
with the prompt that you would like to use to generate the summary.

---

## Future Improvements / Todo
- 🔄 Improve styling (e.g. add a loading spinner)
- 🗄 Add support for more file types (e.g. .txt)
- 🚩 Improve handling of PDFs with complex layouts for accurate audio conversion

---

## Contact / Report a Problem
If you have any feedback or would like to report a bug, please reach out to me via the following email.<br>
Email: aryanr.patel@mail.utoronto.ca

> Built with ❤ by **Aryan Patel** - CS Student & Software Engineer