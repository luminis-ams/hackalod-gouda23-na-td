import json
import os
import threading
from typing import List

import openai
from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

from backend.chains.search_images import search_for_images
from backend.constants import DATA_DIR
from backend.openai import openai_chat_stream, extract_phrases, cache
from backend.openai import openai_chat
from langchain.schema.output import Generation
from elevenlabs import Voice, VoiceSettings, generate
from elevenlabs import set_api_key
from dotenv import load_dotenv
from elevenlabs import play, stream
import multiprocessing
from backend.prompts.extract_terms_prompt import EXTRACT_PROMPT_TEMPLATE

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if os.getenv("ELEVENLABS_API_KEY"):
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))

config = {
    "DEBUG": True,  # some Flask specific configs
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


MIN_FRAGMENT_LENGTH = 40


def read_parallel_queue(queue: multiprocessing.Queue):
    fragment = ''
    while True:
        item = queue.get(block=True)
        if item == "END":
            break

        fragment += item
        if len(fragment) > MIN_FRAGMENT_LENGTH:
            print(fragment)
            yield fragment
            fragment = ''


@app.route("/chat-stream", methods=["POST"])
@cross_origin(origins='*')
def chat_stream():
    global audio_threads

    body = request.json

    def generatez():
        queue = multiprocessing.Queue()

        def read_and_play():
            audio_stream = generate(
                text=read_parallel_queue(queue),
                model="eleven_multilingual_v2",
                stream=True,
                voice=Voice(
                    voice_id='pNInz6obpgDQGcFmaJgB',
                )
            )

            stream(audio_stream)

        proc = multiprocessing.Process(target=read_and_play, args=())
        audio_threads.append(proc)
        proc.start()

        for content in openai_chat_stream(body):
            queue.put(content)
            yield "data: {}\n\n".format(json.dumps({"text": content}))

        queue.put("END")

    return Response(generatez(), mimetype="text/event-stream")


audio_threads: List[multiprocessing.Process] = []


@app.route("/stop-audio", methods=["POST"])
def stop_audio():
    global audio_threads

    for thread in audio_threads:
        while thread.is_alive():
            thread.terminate()

    audio_threads = []

    return Response("OK")


@app.route("/chat", methods=["POST"])
@cross_origin(origins='*')
def chat():
    global audio_threads
    body = request.json
    response = openai_chat(body)

    if os.getenv("ELEVENLABS_API_KEY"):
        text = response['text']
        text = 'In the cases where I want to kill a thread, but do not want to use flags/locks/signals/semaphores/events/whatever, I promote the threads to full blown processes. For code that makes use of just a few threads the overhead is not that bad.'

        def f():
            audio_stream = generate(
                text=text,
                model="eleven_multilingual_v2",
                stream=True,
                voice=Voice(
                    voice_id='pNInz6obpgDQGcFmaJgB',
                    # settings=VoiceSettings(
                    #     # stability=0.71,
                    #     # similarity_boost=0.5,
                    #     style=0.0, use_speaker_boost=True
                    # )
                )
            )

            stream(audio_stream)

        # proc = multiprocessing.Process(target=f, args=())
        # audio_threads.append(proc)
        # proc.start()

    return response


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
