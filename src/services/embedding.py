import os

import openai
from utils.logs import logger
from utils.common import SettingsLoader


class Embeddings:

    APP_NAME = "OPENAI_EMBEDDINGS"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )

    def embed(self, text: str):
        logger.debug("Generating embedding for text %s", text)
        response = openai.Embedding.create(
            model=self.options.get("model"),
            input=text
        )
        logger.debug("Response: %s", response)
        return response.data[0].embedding
