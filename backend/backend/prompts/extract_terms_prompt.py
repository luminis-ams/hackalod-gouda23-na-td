
from langchain.prompts import PromptTemplate

EXTRACT_PROMPT_TEMPLATE = PromptTemplate.from_template(
"""
The user has written the passage below, your goal is to extract the key phrases from the passage which will be used to search for images.
Put each phrase on a new line, and limit the amount of terms to 5. Make the phrases diverse and specific.
Ensure that the phrases overlap as little as possible, and that they are not too similar to each other.
The phrases will be used to search the web for pictures. Take that into account.

Following passage was provided by the user:
```
{{ passage }}
```

List of search phrases is:
""".strip(),
    template_format="jinja2"
)
