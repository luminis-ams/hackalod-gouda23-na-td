import json
import os
from flask import Response

import openai

from langchain.cache import SQLiteCache
from langchain.schema.output import Generation

from backend.prompts.extract_terms_prompt import EXTRACT_PROMPT_TEMPLATE
from backend.story_logic import create_chat_body

cache = SQLiteCache(database_path=".langchain.db")


def openai_chat_stream(body):
    messages = create_chat_body(body)

    for chunk in openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=messages,
            stream=True,

    ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content:
            yield content



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
        max_tokens=200,
    )

    content = response["choices"][0].get("message", {}).get("content")
    cache.update(cache_key, '', [Generation(text=content)])

    return {"text": content}


def extract_phrases(passage):
    if content := cache.lookup(passage, ''):
        return content[0].text.split('\n')

    prompt = EXTRACT_PROMPT_TEMPLATE.format(passage=passage)
    result = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False,
        temperature=1.0,
        max_tokens=200,
    )
    content = result["choices"][0].get("message", {}).get("content")

    cache.update(passage, '', [Generation(text=content)])
    phrases = content.split('\n')

    return phrases
