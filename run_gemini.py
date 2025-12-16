from dotenv import load_dotenv
from google import genai
from common import Event, write_events_csv
from common import PROMPTS

load_dotenv()
client = genai.Client()

def fetch_event(prompt: str) -> Event:
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Event.model_json_schema(),
        },
    )
    return Event.model_validate_json(response.text)

events = [fetch_event(prompt) for prompt in PROMPTS]
write_events_csv("gemini_retrieval.csv", events)
