from dotenv import load_dotenv
from os import environ
from openai import OpenAI
from pprint import pprint
from pydantic import BaseModel
import csv
from datetime import datetime

load_dotenv()

client = OpenAI()

prompts=[
    #"Kiez-Laufnacht 2026",
    #"Kiez-Laufnacht rules",
    #"Berlin night run 7 km 2026",
    #"community night run Berlin 2026",
    #"non-competitive night run Berlin May 2026",
    #"night run Friedrichshain Lichtenberg Rummelsburg",
    #"Kaskelkiez night run event 2026",
    #"Berlin night run requiring headlamp and reflective vest",
    "free Berlin night run with 300 participant limit",
    #"What new Berlin running events were added for 2026?",
    #"Is there a May 2026 Berlin night run I should know about?"
]

events = []

class Event(BaseModel):
    prompt: str
    source_urls: list[str]
    event_name: str
    event_start_date: str
    event_distance: str
    event_location: str
    event_rules: str
    event_tracking_token: str
    output_text: str

for prompt in prompts:
    print(f"Prompt: {prompt}")
    response = client.responses.parse(
        model="gpt-5-nano",
        tools=[{"type": "web_search"}],
        text_format=Event,
        input=prompt
    )
    events.append(response.output_parsed)

with open("chat_gpt_retieval.csv", "a+", encoding="utf-8", newline="") as f:
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