from pydantic import BaseModel
from typing import List
import csv
from datetime import datetime

PROMPTS = [
    #"Kiez-Laufnacht 2026",
    #"Berlin night run 7 km 2026",
    #"community night run Berlin 2026",
    #"non-competitive night run Berlin May 2026",
    #"night run Friedrichshain Lichtenberg Rummelsburg",
    #"Kaskelkiez night run event 2026",
    #"Berlin night run requiring headlamp and reflective vest",
    #"free Berlin night run with 300 participant limit",
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

def sanitize(value: str) -> str:
    if value is None:
        return ""
    return (
        str(value)
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("|", "/")
        .strip()
    )

def write_events_csv(filename: str, events: list[Event]):
    with open(filename, "a+", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        for event in events:
            writer.writerow([
                sanitize(event.prompt),
                datetime.today().strftime("%Y-%m-%d"),
                sanitize(",".join(event.source_urls)),
                sanitize(event.event_name),
                sanitize(event.event_start_date),
                sanitize(event.event_distance),
                sanitize(event.event_location),
                sanitize(event.event_rules),
                sanitize(event.event_tracking_token),
                sanitize(event.output_text),
            ])
