import os

import requests
from bs4 import BeautifulSoup
from PIL import Image

from utils.common import SettingsLoader
from utils.logs import logger

FOLDER_PREFIX = "images/"
WIDTH = 1920
HEIGHT = 1080

class Images:

    APP_NAME = "UNSPLASH"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )

    async def generate(self, section: dict, output_folder: str) -> str:
        os.makedirs(os.path.join(output_folder, FOLDER_PREFIX), exist_ok=True)
        url = f"{self.options.get('source')}{section['topic_slug']}"
        html_response = requests.get(url, timeout=self.options.get("timeout"))
        soup = BeautifulSoup(html_response.text, "html.parser")

        # Find all the images on the page using the img tag
        div = soup.find("div", {"data-test": "search-photos-route"})
        images = div.find_all("img")
        images.pop(0) # This is a garbage file and we don't want it.

        # Get first image from prompt
        first_image = images[0]
        image_url = first_image["src"]
        img_response = requests.get(image_url, timeout=self.options.get("timeout"))

        file_name = f"{section['index']}-{section['topic_slug']}.jpg"
        file_path = os.path.join(output_folder, FOLDER_PREFIX, file_name)
        with open(file_path, "wb") as f:
            f.write(img_response.content)

        image = Image.open(file_path)
        image.thumbnail(
            (self.options.get("width"), self.options.get("height")),
            Image.ANTIALIAS
        )
        image.save(file_path)

        logger.info('Downloaded %s', file_path)
        section['media_path'] = file_path
        return section
