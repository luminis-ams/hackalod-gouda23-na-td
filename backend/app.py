import os

import openai
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin

from backend.chains.search_images import search_for_images
from backend.openai import chat_stream
from backend.openai import openai_chat

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

cors = CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# Sends response back to Deep Chat using the Response format:
# https://deepchat.dev/docs/connect/#Response
@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return {"error": str(e)}, 500


@app.errorhandler(ConnectionError)
def handle_exception(e):
    print(e)
    return {"error": "Internal service error"}, 500


@app.route("/chat", methods=["POST"])
@cross_origin(origins='*')
def chat():
    body = request.json
    return openai_chat(body)


@app.post("/openai-chat-stream")
@cross_origin(origins='*')
def openai_chat_stream():
    body = request.json
    return chat_stream(body)


@app.post("/search_image")
@cross_origin(origins='*')
def search_image():
    body = request.json

    return search_for_images(body['search_for'])


@app.post("/search_person")
@cross_origin(origins='*')
def search_person():
    body = request.json
    person_name = body['person_name']

    person = {
        "surname": "'t Hart",
        "name_first": "56064",
        "father": "Jan",
        "mother": "Catharina van Bemmel",
        "birth_place": "Leiderdorp /Z.H.",
        "birth_data": "",
        "place_of_residence": "Rotterdam",
        "length": "1:667 Meter.",
        "face": "rond",
        "forehead": "gewoon",
        "eyes": "grijs",
        "nose": "gewoon",
        "mouth": "klein",
        "chin": "rond",
        "hair": "blond",
        "eyebrow": "id",
        "features_particular": "ken aan den hals ken aan den hals",
        "events": [
            {"event_date": "1901-12-02", "description": "gegaan aan boord van het SS Prins Hendrik"},
            {"event_date": "1902-12-01",
             "description": "Gedebarkeerd te Batavia en geplaatst bij het 2:e Depot. Bat:on"},
            {"event_date": "1903-05-05", "description": "Overgegaan bij het 5 Bat:on Inf:ie"},
            {"event_date": "1905-07-04", "description": "strafdetachement (bewak: det:t) 5 Bat:en Int:ie"},
            {"event_date": "1906-04-16",
             "description": "faire tegen den vijand of in eene plaats welke dadelijk belegerd of bekend is"},
            {"event_date": "1906-06-01", "description": "ter executie gelegd."},
            {"event_date": "1907-05-18",
             "description": "Van militaire gevangens ontslagen en geplaatst bij het 2:e Depot Bat:en Overgegaan bij het 5 Bat:en Inf:ie"},
            {"event_date": "1908-07-10",
             "description": "bracht, gerekend van en met den dag van inscheping herwaerts naar Nederland te worden opgezonden"}
        ]
    }

    for person_event in person['events']:
        images = search_for_images(person_event["description"])
        person_event["image"] = images[0]["imageOriginal"]

    return person
