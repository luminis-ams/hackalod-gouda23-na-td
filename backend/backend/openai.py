import json
import os
from flask import Response

import openai


def create_chat_body(body):
    # Text messages are stored inside request body using the Deep Chat JSON format:
    # https://deepchat.dev/docs/connect
    return [
        {
            "role": "assistant" if message["role"] == "ai" else message["role"],
            "content": message["text"]
        } for message in body["messages"]
    ]


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
