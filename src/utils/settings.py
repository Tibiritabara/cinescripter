import os
from pathlib import Path
from string import Template


ELEVENLABS = {
    "voice": os.getenv("VOICE_ID"),
    "model": "eleven_monolingual_v1",
}

GIPHY = {
    "api_key": os.getenv("GIPHY_API_KEY"),
    "timeout": 30,
    "max_keywords": 5,
}

UNSPLASH = {
    "source": "https://unsplash.com/s/photos/",
    "width": 1920,
    "height": 1080,
    "timeout": 30,
    "access_key": os.getenv("UNSPLASH_ACCESS_KEY"),
    "secret_key": os.getenv("UNSPLASH_SECRET_KEY"),
}

WEAVIATE = {
    "url": os.getenv("WEAVIATE_HOST"),
    "api_key": os.getenv("WEAVIATE_API_KEY"),
}

# Do we need this if we increase the amount of clips?
OPENAI_SUMMARIZER = {
    "model": "text-davinci-003",
    "temperature": 0,
    "max_tokens": 100,
    "top_p": 1,
    "frequency_penalty": 0.8,
    "presence_penalty": 0,
    "prompt": Template(Path("./prompts/summary.txt").read_text(encoding="utf-8")),
}

OPENAI_EMBEDDINGS = {
    "model": "text-embedding-ada-002",
}

OPENAI_KEYWORDS = {
    "model": "text-davinci-003",
    "temperature": 0.5,
    "max_tokens": 50,
    "top_p": 1,
    "frequency_penalty": 0.8,
    "presence_penalty": 0,
    "prompt": Template(Path("./prompts/keywords.txt").read_text(encoding="utf-8")),
    "max_keywords": 5,
}

OPENAI_SCRIPT = {
    "model": "gpt-3.5-turbo",
    "prompt": Template(Path("./prompts/script.txt").read_text(encoding="utf-8")), 
}

VIDEO = {
    "width": 1920,
    "height": 1080,
}

GENERATOR = {
    "output_folder": "./output/",
}
