from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import csv
from datetime import datetime

load_dotenv()

client = genai.Client()

prompts=[
    #"Kiez-Laufnacht 2026",
    #"Kiez-Laufnacht rules",
    "Berlin night run 7 km 2026",
    #"community night run Berlin 2026",
    #"non-competitive night run Berlin May 2026",
    #"night run Friedrichshain Lichtenberg Rummelsburg",
    #"Kaskelkiez night run event 2026",
    #"Berlin night run requiring headlamp and reflective vest",
    #"free Berlin night run with 300 participant limit",
    #"What new Berlin running events were added for 2026?",
    #"Is there a May 2026 Berlin night run I should know about?"
]

events = []

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

for prompt in prompts:
    print(f"Prompt: {prompt}")

    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Event.model_json_schema(),
        },
    )
    events.append(Event.model_validate_json(response.text))

with open("gemini_retrieval.csv", "a+", encoding="utf-8", newline="") as f:
    for event in events:
        writer = csv.writer(f, delimiter="|")
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