import os

from backend.chains.search_images import search_for_images
from backend.openai import cache, extract_phrases
from backend.prompts.extract_terms_prompt import EXTRACT_PROMPT_TEMPLATE
import openai
from dotenv import load_dotenv
from langchain.schema.output import Generation

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

passagez = """
Act 1:

Als het zonlicht de hemel boven Nederland begint te verlichten, wordt daar op een rustige ochtend in het jaar 1883 een kind geboren. Het is een jongen, Johannes, geboren in de stad Wageningen, gelegen in de provincie Gelderland. Zijn ouders, vader en moeder, heten respectievelijk Willemina en Oudsen. Zij hebben zich altijd gewijd aan hard werken en hebben veel liefde en zorg voor hun zoon.

Johannes groeit op in de warme omgeving van Wageningen en wordt omringd door de schoonheid van de natuur om hem heen. Hij ontwikkelt een nieuwsgierigheid naar de wereld en een verlangen naar avontuur. Tijd gaat voorbij en als Johannes de leeftijd van 19 bereikt, voelt hij dat het tijd is om zijn vleugels uit te slaan. Hij heeft altijd al gedroomd van verre landen en opwindende ontdekkingen. Wanneer hij de kans krijgt om bij het leger te gaan, twijfelt hij geen moment en sluit hij zich aan bij het korps van de marine.

Met zijn bagage in de hand, zijn ouders aan zijn zijde en de gedachte aan alle mogelijkheden die de toekomst biedt, maakt Johannes zich klaar om aan een ongelooflijke reis te beginnen. Hij vertrekt uit Wageningen, zijn geboorteplaats, met een mengeling van opwinding en een
"""

phrases = extract_phrases(passagez)


images = []
for phrase in phrases:
    images.extend(search_for_images(phrase, return_metadata=False))

images = sorted(images, key=lambda x: x.metadata['score'], reverse=True)
unique_images = []
seen = {}
for image in images:
    if image.metadata['handleURI'] not in seen:
        unique_images.append(image)
        seen[image.metadata['handleURI']] = True

result_images = unique_images[:5]
result_images = [image.metadata for image in result_images]