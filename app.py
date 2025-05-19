import os
from flask import Flask, render_template, request, redirect, session, Response
from flask_session import Session
from PyPDF2 import PdfReader
from gtts import gTTS
from google import genai
from dotenv import load_dotenv
from database import initialize_database, save_to_database, get_audio_from_database
from io import BytesIO

load_dotenv()  # load the environment variables

app = Flask(__name__)

# intial setup for sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# intial setup for database
initialize_database()

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
    buffer = BytesIO()
    audio.write_to_fp(buffer)
    bytes = buffer.getvalue()

    # storing into the database
    audio_id = save_to_database(bytes)  
    
    # generate summary using gemini
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[text_content, os.getenv("PROMPT")],
    )

    # store the response and file_id in a session and redirect the user to result page
    session["summary"] = response.text
    session["audio_id"] = audio_id
    return redirect("/result")
    

@app.route("/result")
def result():
    summary = session["summary"]
    audio_id = session["audio_id"]
    return render_template("result.html", summary=summary, audio_id=audio_id)


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/audio/<int:audio_id>")
def get_audio(audio_id):
    audio_bytes = get_audio_from_database(audio_id)
    if audio_bytes:
        return Response(audio_bytes, mimetype="audio/mpeg")
    return redirect("/error")