import json
from pathlib import Path

from backend.prompts.story_page_prompt import STORY_PROMPT_TEMPLATE


def test_story_prompt():
    data = json.loads(Path('/home/egordm/Projects/workshops/hackalod-gouda23-na-td/data/suppleties_cleaned/nl_zh_ha_na-2_10_50-505_4_page_data.json').read_text())

    prompt = STORY_PROMPT_TEMPLATE.format(
        **data
    )

    print(prompt)

data = json.loads(Path('/home/egordm/Projects/workshops/hackalod-gouda23-na-td/data/suppleties_cleaned/nl_zh_ha_na-2_10_50-505_4_page_data.json').read_text())

prompt = STORY_PROMPT_TEMPLATE.format(
    **data
)

print(prompt)