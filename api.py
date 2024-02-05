from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from TTS.api import TTS
import elevenlabs

from brain import Brain
import hashlib
import base64
import os

app = Flask(__name__)
CORS(app)
brain = Brain("test")

# not available in the free tier
# goldfinger_voice = elevenlabs.clone(
#     name="Goldfinger",
#     description="An old Dutch male voice who speaks english with a strong accent", # Optional
#     files=["./goldfinger1.wav"],
# )

@app.route("/ask", methods=['POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def query():
    return '' if "query" not in request.json else json_response(brain.recall(request.json.get('query')))

@app.route("/tell", methods=['POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def store():
    return '' if 'text' not in request.json else json_response(brain.store(request.json.get('text')))

@app.route("/tts", methods=['POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def tts():
    if 'text' not in request.json:
        return ''
    else:
        text_to_speak = request.json.get('text')
        speech_file = convert_text_to_speech(text_to_speak)

        return send_file(
          speech_file, 
          mimetype="audio/wav",
          as_attachment=True,
          download_name="test.wav"
        )

def json_response(payload, status=200):
    return (jsonify(payload), status, {'content-type': 'application/json'})

def audio_file(text):
    hasher = hashlib.sha1(text.encode('utf-8'))
    slug = "-".join(text.split()[:4]) + "-" + base64.urlsafe_b64encode(hasher.digest()[:10]).decode("ascii")
    return f'audio/{slug}.wav'

def convert_text_to_speech(text):
    # check to see if audio file already exists and return it if it does
    file_name = audio_file(text)

    if not os.path.exists(file_name):
        speech_bytes = elevenlabs.generate(text)
        speech_file = elevenlabs.save(speech_bytes, file_name)

    return file_name