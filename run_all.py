from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import csv
from datetime import datetime
from openai import OpenAI
from perplexity import Perplexity
from google import genai

PROMPTS = [
    "Kiez-Laufnacht 2026",
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

def write_event_csv(event: Event, platform: str):
    with open("retrievals.csv", "a+", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow([
            sanitize(platform),
            sanitize(event.prompt),
            datetime.now(),
            sanitize(",".join(event.source_urls)),
            sanitize(event.event_name),
            sanitize(event.event_start_date),
            sanitize(event.event_distance),
            sanitize(event.event_location),
            sanitize(event.event_rules),
            sanitize(event.event_tracking_token),
            sanitize(event.output_text),
        ])

def fetch_chatgpt(prompt: str) -> Event:
    client = OpenAI()
    response = client.responses.parse(
        model="gpt-5-nano",
        tools=[{"type": "web_search"}],
        text_format=Event,
        input=prompt,
    )
    return response.output_parsed

def fetch_gemini(prompt: str) -> Event:
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Event.model_json_schema(),
        },
    )
    return Event.model_validate_json(response.text)

def fetch_perplexity(prompt: str) -> Event:
    client = Perplexity()
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

if __name__ == "__main__":
    load_dotenv()
    print("----------START----------")
    for p in PROMPTS:
        print(f"[{datetime.now()}] Prompt: {p}")
        print(f"[{datetime.now()}] Running Chat GPT...")
        write_event_csv(fetch_chatgpt(p), "chatgpt")
        print(f"[{datetime.now()}] Running Gemini...")
        write_event_csv(fetch_gemini(p), "gemini")
        print(f"[{datetime.now()}] Running Perplexity...")
        write_event_csv(fetch_perplexity(p), "perplexity")
    print("----------END----------")
