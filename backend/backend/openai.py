import json
import os
from flask import Response

import openai

from langchain.cache import SQLiteCache
from langchain.schema.output import Generation
from backend.story_logic import create_chat_body

cache = SQLiteCache(database_path=".langchain.db")

def chat_stream(body):
    messages = create_chat_body(body)


    def generate():
        for chunk in openai.ChatCompletion.create(
                model=os.getenv("OPENAI_MODEL"),
                messages=messages,
                stream=True,

        ):
            content = chunk["choices"][0].get("delta", {}).get("content")
            if content:
                yield "data: {}\n\n".format(json.dumps({"text": content}))

    return Response(generate(), mimetype="text/event-stream")


def openai_chat(body):
    messages = create_chat_body(body)

    cache_key = json.dumps(messages)
    if content := cache.lookup(cache_key, ''):
        return {"text": content[0].text}

    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=messages,
        stream=False,
        temperature=1.0,
        max_tokens=350,
    )

    content = response["choices"][0].get("message", {}).get("content")
    cache.update(cache_key, '', [Generation(text=content)])

    return {"text": content}


