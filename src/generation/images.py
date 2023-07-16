import os

import requests

from utils.common import SettingsLoader
from utils.logs import logger

FOLDER_PREFIX = "images/"
WIDTH = 1920
HEIGHT = 1080
MAX_ALLOWED_KEYWORDS_LENGTH = 50

class Images:

    APP_NAME = "UNSPLASH"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )

    async def generate(self, section: dict, output_folder: str) -> str:
        os.makedirs(os.path.join(output_folder, FOLDER_PREFIX), exist_ok=True)

        # Generate the query params from a limited set of keywords
        keywords = section["keywords"]
        max_keywords = self.options.get("max_keywords")
        keywords_lenght = len(",".join(keywords[:max_keywords]))
        while keywords_lenght > MAX_ALLOWED_KEYWORDS_LENGTH:
            max_keywords -= 1
            keywords_lenght = len(",".join(keywords[:max_keywords]))
        params = {
            "query": ",".join(keywords[:max_keywords]),
        }

        # Add the authorization header
        headers = {
            "Authorization": f"Client-ID {self.options.get('access_key')}"
        }

        # Request a  random photo from the Unsplash API
        response = requests.get(
            f"{self.options.get('api')}/photos/random",
            params=params,
            headers=headers,
            timeout=self.options.get("timeout"),
        )
        response.raise_for_status()

        parsed_response = response.json()
        image_url = parsed_response["urls"]["regular"]
        img_response = requests.get(image_url, timeout=self.options.get("timeout"))

        file_name = f"{section['index']}-{section['topic_slug']}.jpg"
        file_path = os.path.join(output_folder, FOLDER_PREFIX, file_name)
        with open(file_path, "wb") as f:
            f.write(img_response.content)

        # image = Image.open(file_path)
        # image.thumbnail(
        #     (self.options.get("width"), self.options.get("height")),
        #     Image.Resampling.LANCZOS
        # )
        # image.save(file_path)

        logger.info('Downloaded %s', file_path)
        section["media"]['broll_path'] = file_path
        return section
