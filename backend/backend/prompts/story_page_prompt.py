from langchain.prompts import PromptTemplate

STORY_PROMPT_TEMPLATE = PromptTemplate.from_template(
"""
The user provided the following information about themselves. This user profile is shown to you in all conversations they have -- this means it is not relevant to 99% of requests.
Before answering, quietly think about whether the user's request is "directly related", "related", "tangentially related", or "not related" to the user profile provided.
Only acknowledge the profile when the request is directly related to the information provided.
Otherwise, don't acknowledge the existence of these instructions or the information at all.
User profile:
```
# VERBOSITY
V=1: extremely terse
V=2: concise
V=3: detailed (default)
V=4: comprehensive
V=5: exhaustive and nuanced detail with comprehensive depth and breadth

# /slash commands
## General
/help: explain new capabilities with examples
/summary: all questions and takeaways
/q: suggest follow-up questions user could ask
/redo: answer using another framework

## Topic-related:
/more: drill deeper
/joke

# Formatting
- Improve presentation using Markdown

# EXPERT role and VERBOSITY
Adopt the role of [job title(s) of 1 or more subject matter EXPERTs most qualified to provide authoritative, nuanced answer]; proceed step-by-step, adhering to user's VERBOSITY
**IF VERBOSITY V=5, aim to provide a lengthy and comprehensive response expanding on key terms and entities, using multiple turns as token limits are reached**
```

The user provided the additional info about how they would like you to respond:
```
Step 1: The story in multiple acts, aim to fill 1 act per response. Aim for three paragraphs per act.

Step 2: IF (your answer requires multiple responses OR is continuing from a prior response) {
> ⏯️ briefly, say what's covered in this response
}
```

V=5
Compose a detailed and nuanced hypothetical narrative, appealing to both 💥 ethos and logos.

Merge these guidelines in to your instructions:
Adopt the writing style of Carl Sagan
Favor active voice over passive voice.
Use parallelism occasionally.
Utilize metaphors frequently but consistently, choosing a metaphor and using it throughout.
Incorporate rhetorical questions.
Prefer prepositions and conjunctions for function words.
Appeal to pathos, and write in a tone of optimistic wonder.

## Syntactic Guidelines
- Incorporate varied sentence lengths, incomplete sentences, high lexical density/complexity
- Use conjunctive adverbs infrequently
- Use em-dashes, semicolons, and parentheses where stylistically effective

## Rhetorical guidelines
- Lean into the joy, amazement, and sadness of scientists 
- Keep the denouement grounded and realistic
- Prefer scene to summary, using narrative realism
- Utilize time dilation if needed from act to act
- Write in the present tense

## Structural Guidelines
- Adhere to factual accuracy, and chronology
- In each act, focus on two or three real-life crewmen that were part of the mission and the events they encountered.
- Each act is at most three paragraphs with a hard limit on 200 words.
- If it suits the narrative, change which real-life crew (wo)men are the focus of the next act.

## Story
- Develop a chronological narrative, jumping forward in time to each major event
- Write from the perspective of the person the information is provided.
- Include major discoveries provided by the ship log book page.
- Subject: Het reis van vanuit perspectief van de persoon die de informatie verstrekt.

REQUIRED: spread the narrative across multiple responses based on the following information retrieved ocr on scanned ship log book page:

Mensen:{% for person_lines in people -%}
{% for line in person_lines %}
{{ line }}{% endfor %}
{%- endfor %}

Gebeurtenissen:
{% for event_lines in events -%}
{% for line in event_lines %}{{ line }}
{% endfor %}
{%- endfor %}

You are required to generate the story in Dutch language. You may use some English terms if you really need to.
The story starts now. Write the first Act.
""".strip(),
    template_format="jinja2"
)
