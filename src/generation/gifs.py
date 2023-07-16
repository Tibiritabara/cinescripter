import os

import requests
import random

from utils.common import SettingsLoader
from utils.logs import logger

FOLDER_PREFIX = "gifs/"
MAX_ALLOWED_KEYWORDS_LENGTH = 50

class Gifs:

    APP_NAME = "GIPHY"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )
    
    async def generate(self, section: dict, output_folder: str) -> str:
        os.makedirs(os.path.join(output_folder, FOLDER_PREFIX), exist_ok=True)
        keywords = section["keywords"]
        # tag = random.choice(keywords)
        tag = ", ".join(keywords)
        params = {
            "api_key": self.options.get("api_key"),
            "s": tag,
        }
    
        response = requests.get(
            f"{self.options.get('api')}/v1/gifs/translate",
            params=params,
            timeout=self.options.get("timeout"),
        )
        response.raise_for_status()

        parsed_response = response.json()
        image_url = parsed_response["data"]["images"]["original_mp4"]["mp4"]
        img_response = requests.get(
            image_url,
            timeout=self.options.get("timeout")
        )
        file_name = f"{section['index']}-{section['topic_slug']}.mp4"
        file_path = os.path.join(output_folder, FOLDER_PREFIX, file_name)
        with open(file_path, "wb") as fl:
            fl.write(img_response.content)
        logger.info('Tag: %s, Keywords: %s, Downloaded %s', tag, keywords, file_path)
        section["media"]["broll_path"] = file_path
        return section
