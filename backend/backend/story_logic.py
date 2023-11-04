from backend.prompts.story_page_prompt import STORY_PROMPT_TEMPLATE


def create_chat_body(body):
    # Text messages are stored inside request body using the Deep Chat JSON format:
    # https://deepchat.dev/docs/connect

    input_messages = body["messages"]
    assert len(input_messages) > 0

    messages = []
    story_page_data = input_messages[0]["story_page_data"]

    story_prompt = STORY_PROMPT_TEMPLATE.format(**story_page_data)

    if len(input_messages) == 1:
        messages.append({
            "role": "user",
            "content": story_prompt
        })
    else:
        messages.append({
            "role": "system",
            "content": story_prompt
        })

    messages.extend([
        {
            "role": "assistant" if message["role"] == "ai" else message["role"],
            "content": message["text"]
        } for message in input_messages
        if 'role' in message and 'text' in message
    ])

    return messages
