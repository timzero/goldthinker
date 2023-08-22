from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from TTS.api import TTS

from brain import Brain

app = Flask(__name__)
CORS(app)
brain = Brain("test")

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
        tts_model = TTS(
            model_name="tts_models/multilingual/multi-dataset/your_tts",
            progress_bar=False,
            gpu=True
        )

        tts_model.tts_to_file(
            request.json.get('text'),
            speaker_wav="goldfinger1.wav",
            language="en",
            file_path="output.wav"
        )

        return send_file(
          "output.wav", 
          mimetype="audio/wav",
          as_attachment=True,
          download_name="test.wav"
        )

def json_response(payload, status=200):
    return (jsonify(payload), status, {'content-type': 'application/json'})
