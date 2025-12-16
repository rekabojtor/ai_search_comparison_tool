from dotenv import load_dotenv
from run_perplexity import Perplexity
from common import Event, write_events_csv
from common import PROMPTS

load_dotenv()
client = Perplexity()

def fetch_event(prompt: str) -> Event:
    response = client.chat.completions.create(
        model="sonar",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "schema": Event.model_json_schema()
            },
        },
    )
    return Event.model_validate_json(response.choices[0].message.content)

events = [fetch_event(prompt) for prompt in PROMPTS]
write_events_csv("perplexity_retrieval.csv", events)
