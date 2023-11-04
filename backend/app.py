import json
import os
import threading

import openai
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin

from backend.chains.search_images import search_for_images
from backend.constants import DATA_DIR
from backend.openai import chat_stream, extract_phrases, cache
from backend.openai import openai_chat
from langchain.schema.output import Generation
from elevenlabs import Voice, VoiceSettings, generate
from elevenlabs import set_api_key
from dotenv import load_dotenv
from elevenlabs import play, stream
from backend.prompts.extract_terms_prompt import EXTRACT_PROMPT_TEMPLATE



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if os.getenv("ELEVENLABS_API_KEY"):
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))


config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


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
    response =  openai_chat(body)

    text = response['text']

    if os.getenv("ELEVENLABS_API_KEY"):
        def f():
            audio_stream = generate(
                text=text,
                model="eleven_multilingual_v2",
                voice=Voice(
                    voice_id='pNInz6obpgDQGcFmaJgB',
                    # settings=VoiceSettings(
                    #     # stability=0.71,
                    #     # similarity_boost=0.5,
                    #     style=0.0, use_speaker_boost=True
                    # )
                )
            )

            play(audio_stream)

        t1 = threading.Thread(target=f)
        t1.start()

    return response


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


@app.post("/extract_images")
@cross_origin(origins='*')
def extract_images():
    body = request.json

    if hit := cache.lookup(json.dumps(body['passage']), ''):
        return {"images": json.loads(hit[0].text)}

    passage = body['passage']
    phrases = extract_phrases(passage)

    images = []
    for phrase in phrases:
        images.extend(search_for_images(phrase, return_metadata=False))

    images = sorted(images, key=lambda x: x.metadata['score'], reverse=True)
    unique_images = []
    seen = {}
    for image in images:
        if image.metadata['handleURI'] not in seen:
            unique_images.append(image)
            seen[image.metadata['handleURI']] = True

    result_images = unique_images[:5]
    result_images = [image.metadata for image in result_images]

    cache.update(json.dumps(body['passage']), '', [Generation(text=json.dumps(result_images))])

    return {"images": result_images}

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


def load_person_from_file(person_name: str):
    print(f"Loading person: {person_name}")

    with open(DATA_DIR / f"curated/{person_name}.json", 'r') as file:
        data = file.read()

    return json.loads(data)
