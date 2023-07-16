import os
from pathlib import Path
from string import Template

PROMPTS_PATH = os.getenv("PROMPTS_PATH", "./prompts/")

ELEVENLABS = {
    "voice": os.getenv("VOICE_ID"),
    "model": "eleven_multilingual_v1",
}

GIPHY = {
    "api_key": os.getenv("GIPHY_API_KEY"),
    "timeout": 30,
    "max_keywords": 5,
    "api": "https://api.giphy.com"
}

UNSPLASH = {
    "source": "https://unsplash.com/s/photos/",
    "width": 1920,
    "height": 1080,
    "timeout": 30,
    "access_key": os.getenv("UNSPLASH_ACCESS_KEY"),
    "secret_key": os.getenv("UNSPLASH_SECRET_KEY"),
    "api": "https://api.unsplash.com",
    "max_keywords": 5,
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
    "prompt": Template(Path(os.path.join(PROMPTS_PATH, "summary.txt")).read_text(encoding="utf-8")),
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
    "prompt": Template(Path(os.path.join(PROMPTS_PATH, "keywords.txt")).read_text(encoding="utf-8")),
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

LOGS = {
    "level": os.getenv("LOG_LEVEL", "DEBUG")
}
