import os

import giphy_client
import requests

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
        api_instance = giphy_client.DefaultApi()
        keywords = section["keywords"]
        max_keywords = self.options.get("max_keywords")
        keywords_lenght = len(",".join(keywords[:max_keywords]))
        while keywords_lenght > MAX_ALLOWED_KEYWORDS_LENGTH:
            max_keywords -= 1
            keywords_lenght = len(",".join(keywords[:max_keywords]))
        api_response = api_instance.gifs_search_get(
            self.options.get("api_key"),
            ",".join(keywords[:max_keywords]),
            limit=1
        )
        gif = api_response.data[0]
        image_url = gif.images.original.mp4
        img_response = requests.get(
            image_url,
            timeout=self.options.get("timeout")
        )
        file_name = f"{section['index']}-{section['topic_slug']}.mp4"
        file_path = os.path.join(output_folder, FOLDER_PREFIX, file_name)
        with open(file_path, "wb") as fl:
            fl.write(img_response.content)
        logger.info('Downloaded %s', file_path)
        section["media_path"] = file_path
        return section
