from run_chatgpt import fetch_event as fetch_chatgpt
from run_gemini import fetch_event as fetch_gemini
from run_perplexity import fetch_event as fetch_perplexity
from common import write_events_csv
from common import PROMPTS

def run(provider_name: str, fetch_fn, output_file: str):
    events = [fetch_fn(prompt) for prompt in PROMPTS]
    write_events_csv(output_file, events)

if __name__ == "__main__":
    run("chatgpt", fetch_chatgpt, "chatgpt_retrieval.csv")
    run("gemini", fetch_gemini, "gemini_retrieval.csv")
    run("perplexity", fetch_perplexity, "perplexity_retrieval.csv")
