import json
from pathlib import Path

from backend.prompts.story_page_prompt import STORY_PROMPT_TEMPLATE



data = json.loads(Path('/home/egordm/Projects/workshops/hackalod-gouda23-na-td/data/curated/four.json').read_text())

prompt = STORY_PROMPT_TEMPLATE.format(
    **data
)

print(prompt)