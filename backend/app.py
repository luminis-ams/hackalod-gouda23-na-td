import os

from flask import Flask
from flask import Flask, request

from backend.openai import chat_stream, openai_chat
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import openai

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
