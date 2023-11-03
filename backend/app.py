from flask import Flask
from flask import Flask, request
from backend.services import OpenAI
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

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


open_ai = OpenAI()


@app.post("/openai-chat")
def openai_chat():
    body = request.json
    return open_ai.chat(body)


@app.post("/openai-chat-stream")
def openai_chat_stream():
    body = request.json
    print('hello')
    return open_ai.chat_stream(body)


@app.post("/openai-image")
def openai_image():
    files = request.files.getlist("files")
    return open_ai.image_variation(files)
