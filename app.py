import os
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from PyPDF2 import PdfReader
from gtts import gTTS
from google import genai
from dotenv import load_dotenv

load_dotenv()  # load the environment variables

app = Flask(__name__)

# intial setup for sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    session.clear()  # clear session data to prevent any old data from being displayed
    # GET
    if request.method == "GET":
        return render_template("upload.html")

    # POST
    file = request.files.get("fileInput")
    text = request.form.get("textInput")
    text_content = ""

    # only proceed if the uploaded file is a pdf
    if file and file.filename.endswith(".pdf"):
        # extract text
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content += page_text

    # process the text if the user pasted the text
    elif text:
        text_content = text

    else:
        return redirect("/error")
    
    # convert text to audio
    audio = gTTS(text_content, lang="en")
    audio.save("static/audio.mp3")
    
    # generate summary using gemini
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[text_content, os.getenv("PROMPT")],
    )

    # store the response in a session and redirect the user to result page
    session["summary"] = response.text
    return redirect("/result")
    

@app.route("/result")
def result():
    summary = session["summary"]
    return render_template("result.html", summary=summary)


@app.route("/error")
def error():
    return render_template("error.html")
