import json
from pathlib import Path

import jinja2
from collections import OrderedDict
import requests
import io
import base64
from PIL import Image

# PRompt to generate image based on the features in json
# Do not include feature if not present (using jinja)
BASE_PROMPT = """
Visualize a highly detailed, realistic image of a 19th-century antique bronze medallion, approximately the size of a large coin. 
The medallion should have a rich, polished surface with a slightly weathered, brushed finish to emphasize its age. 
It will depict a crew member of a ship from 18th century. 
Engraved into the center of the medallion is the portrait of a person, captured in profile.
The person should be based on the following description:
Name: {{ name_first }} {{ surname }}
{% if birth_place %}Birth place: {{ birth_place }}{% endif %}
{% if birth_data %}Birth date: {{ birth_data }}{% endif %}
{% if place_of_residence %}Place of residence: {{ place_of_residence }}{% endif %}
{% if length %}Length: {{ length }}{% endif %}
{% if face %}Face: {{ face }}{% endif %}
{% if forehead %}Forehead: {{ forehead }}{% endif %}
{% if eyes %}Eyes: {{ eyes }}{% endif %}
{% if nose %}Nose: {{ nose }}{% endif %}
{% if mouth %}Mouth: {{ mouth }}{% endif %}
{% if chin %}Chin: {{ chin }}{% endif %}
{% if hair %}Hair: {{ hair }}{% endif %}
{% if eyebrow %}Eyebrow: {% if eyebrow.lower() == 'ider' or eyebrow.lower() == 'id' %}wide{% else %}narrow{% endif %}{% endif %}
{% if features_particular %}Features particular: {{ features_particular }}{% endif %}

Do not include any text on the medallion. <lora:Cnl-XL-V1:0.5>
""".strip()

batch_size = 3
payload = {
    "prompt": None,
    "negative_prompt": "text, year",
    "steps": 30,
    "batch_size": batch_size,
    "cfg_scale": 4.0,
    "sampler_index": "Euler a",
    "width": 1024,
    "height": 1024,
}

def generate_image(input, key):
    prompt = env.from_string(BASE_PROMPT).render(**input)
    with open(f'../../data/curated/{key}.txt', 'w') as f:
        f.write(prompt)

    payload_now = {
        **payload,
        'prompt': prompt.strip()
    }

    print(f'Generating image for {key}')
    response = requests.post(url=f'http://192.168.1.111:7860/sdapi/v1/txt2img', json=payload_now)

    r = response.json()
    for i in range(batch_size):
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][i])))
        image.save(f'../../data/curated/{key}_{i}.png')


env = jinja2.Environment()


data = {}
for file in Path('/home/egordm/Projects/workshops/hackalod-gouda23-na-td/data/curated').glob('*.json'):
    with open(file, 'r') as f:
        print(f'Loading {file.stem}')
        data[file.stem] = json.load(f, object_pairs_hook=OrderedDict)['person']
        u = 0


prompts = []
for key, value in data.items():
    prev = None
    prev_value = None
    for k, v in value.items():
        if v.startswith('id'):
            value[k] = prev_value if prev_value else v

        prev = k
        prev_value = v


    generate_image(value, key)

print(prompts[2])


