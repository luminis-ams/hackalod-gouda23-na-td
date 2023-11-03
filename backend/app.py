import os

from flask import Flask
from flask import Flask, request

from backend.openai import chat_stream
from flask_cors import CORS
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

cors = CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


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


@app.post("/openai-chat-stream")
def openai_chat_stream():
    body = request.json
    print('hello')
    # return open_ai.chat_stream(body)
    return chat_stream(body)
