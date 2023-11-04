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

    person = load_person_from_file(person_name)

    for person_event in person['events']:
        images = search_for_images(person_event["description"])
        person_event["image"] = images[0]["imageOriginal"]

    return person
