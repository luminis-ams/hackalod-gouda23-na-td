import requests
import io
import base64
from PIL import Image

payload = {
    "prompt": """
Visualize a highly detailed, realistic image of a 19th-century antique bronze medallion, approximately the size of a large coin. 
The medallion should have a rich, polished surface with a slightly weathered, brushed finish to emphasize its age. 
It will depict a crew member of a ship from 18th century. 
Engraved into the center of the medallion is the portrait of a person, captured in profile.
The person should be based on the following description:
Name: Joannes Smeekes
Birth place: Maastricht / Limburg
Birth date: 2 December 1870
Place of residence: den, oder nicht sein, nicht  <lora:Cnl-XL-V1:0.2>
Length: „
    """.strip(),
    "negative_prompt": "text, year",
    "steps": 30,
    # "batch_size": 3,
    "cfg_scale": 4.0,
    "sampler_index": "Euler a",
    "width": 1024,
    "height": 1024,
}

response = requests.post(url=f'http://192.168.1.111:7860/sdapi/v1/txt2img', json=payload)


r = response.json()
image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
image.save('output.png')