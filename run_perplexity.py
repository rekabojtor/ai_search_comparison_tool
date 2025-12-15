from perplexity import Perplexity
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import csv
from datetime import datetime

load_dotenv()

client = Perplexity()

prompts=[
    "Kiez-Laufnacht 2026",
    #"Kiez-Laufnacht rules",
    #"Berlin night run 7 km 2026",
    #"community night run Berlin 2026",
    #"non-competitive night run Berlin May 2026",
    #"night run Friedrichshain Lichtenberg Rummelsburg",
    #"Kaskelkiez night run event 2026",
    #"Berlin night run requiring headlamp and reflective vest",
    #"free Berlin night run with 300 participant limit",
    #"What new Berlin running events were added for 2026?",
    #"Is there a May 2026 Berlin night run I should know about?"
]

class Event(BaseModel):
    prompt: str
    source_urls: List[str]
    event_name: str
    event_start_date: str
    event_distance: str
    event_location: str
    event_rules: str
    event_tracking_token: str
    output_text: str

events = []

for prompt in prompts:
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
    event = Event.model_validate_json(response.choices[0].message.content)
    events.append(event)

with open("perplexity_retrieval.csv", "a+", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="|")
    for event in events:
        writer.writerow([
            event.prompt,
            datetime.today().strftime('%Y-%m-%d'),
            ",".join(event.source_urls),
            event.event_name,
            event.event_start_date,
            event.event_distance,
            event.event_location,
            event.event_rules,
            event.event_tracking_token,
            event.output_text,
        ])