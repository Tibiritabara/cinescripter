import os

import requests
from bs4 import BeautifulSoup
from slugify import slugify

from generation.keywords import Keyword
from utils.logs import logger
from PIL import Image


SOURCE = "https://unsplash.com/s/photos/"
FOLDER_PREFIX = "images/"
TIMEOUT = 30
WIDTH = 1920
HEIGHT = 1080

class Images:
    def __init__(self, sort, topic, output_folder):
        self.sort = sort
        self.topic = topic
        self.output_folder = output_folder

    def generate(self,):
        os.makedirs(os.path.join(self.output_folder, FOLDER_PREFIX), exist_ok=True)
        keyword = Keyword(self.topic).generate()
        topic_slug = slugify(keyword)
        url = f"{SOURCE}{topic_slug}"
        html_response = requests.get(url, timeout=TIMEOUT)
        soup = BeautifulSoup(html_response.text, "html.parser")

        # Find all the images on the page using the img tag
        div = soup.find("div", {"data-test": "search-photos-route"})
        images = div.find_all("img")
        images.pop(0) # This is a garbage file and we don't want it.

        # Get first image from prompt
        first_image = images[0]
        image_url = first_image["src"]
        img_response = requests.get(image_url, timeout=TIMEOUT)

        file_name = f"{self.sort}-{topic_slug}.jpg"
        file_path = os.path.join(self.output_folder, FOLDER_PREFIX, file_name)
        with open(file_path, "wb") as f:
            f.write(img_response.content)

        image = Image.open(file_path)
        image.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)
        image.save(file_path)

        logger.info('Downloaded %s', file_path)
        return file_path
