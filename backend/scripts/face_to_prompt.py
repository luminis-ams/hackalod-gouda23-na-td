import json
import jinja2
from collections import OrderedDict

# Example entry
# "5101": {
#     "surname": "Leuffgen",
#     "name_first": "Geo",
#     "father": "Joseph",
#     "mother": "Caroline Windeck",
#     "birth_place": "St Veth (Duitsch",
#     "birth_data": "28 December 1871",
#     "place_of_residence": "LaatstSt. Vith",
#     "length": "163 Meter",
#     "face": "ovaal",
#     "forehead": "gewoon",
#     "eyes": "grijs",
#     "nose": "gewoon",
#     "mouth": "idem",
#     "chin": "rond",
#     "hair": "bruin",
#     "eyebrow": "ider",
#     "features_particular": ""
# },

# PRompt to generate image based on the features in json
# Do not include feature if not present (using jinja)
BASE_PROMPT = """
Generate a portrait of a person based on the following features:
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
""".strip()

with open('../../data/nl_zh_ha_na-2_10_50-505_data_structured_2023-11-03_18-08-30.json', 'r') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)


print(data)

env = jinja2.Environment()

prompts = []
for key, value in data.items():
    prev = None
    prev_value = None
    for k, v in value.items():
        if v.startswith('id'):
            value[k] = prev_value if prev_value else v

        prev = k
        prev_value = v


    prompts.append(env.from_string(BASE_PROMPT).render(**value))

print(prompts[2])
