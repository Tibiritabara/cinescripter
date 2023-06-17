import os

import openai
from utils.logs import logger

SAMPLE_PROMPT = "write one keyword from this text:\n\n%s"

class Keyword:
    def __init__(self, prompt):
        self.prompt = prompt

    def generate(self,):
        logger.debug("Generating keyword for prompt: %s", self.prompt)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=SAMPLE_PROMPT % self.prompt,
            # prompt=f"{SAMPLE_PROMPT}The quick brown fox jumps over the lazy dog.",
            temperature=0.5,
            max_tokens=5,
            top_p=1,
            frequency_penalty=0.8,
            presence_penalty=0
        )
        keyword = response.choices[0].text.replace('\n', '').rstrip().lower()
        logger.debug("Generated keyword: %s", keyword)
        return keyword
