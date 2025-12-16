from dotenv import load_dotenv
from openai import OpenAI
from common import Event, write_events_csv
from common import PROMPTS

load_dotenv()
client = OpenAI()

def fetch_event(prompt: str) -> Event:
    response = client.responses.parse(
        model="gpt-5-nano",
        tools=[{"type": "web_search"}],
        text_format=Event,
        input=prompt,
    )
    return response.output_parsed

events = [fetch_event(prompt) for prompt in PROMPTS]
write_events_csv("chatgpt_retrieval.csv", events)
