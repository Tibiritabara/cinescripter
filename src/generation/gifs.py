import os

import requests
from bs4 import BeautifulSoup
from slugify import slugify

from generation.keywords import Keyword
from utils.logs import logger
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint


FOLDER_PREFIX = "gifs/"
TIMEOUT = 30

class Gifs:
    def __init__(self, sort, topic, output_folder):
        self.sort = sort
        self.topic = topic
        self.output_folder = output_folder

    def generate(self,):
        os.makedirs(os.path.join(self.output_folder, FOLDER_PREFIX), exist_ok=True)
        keyword = Keyword(self.topic).generate()
        topic_slug = slugify(keyword)
        api_instance = giphy_client.DefaultApi()
        api_response = api_instance.gifs_search_get(
            os.getenv("GIPHY_API_KEY"),
            keyword,
            limit=1
        )
        gif_id = api_response.data[0]
        image_url = gif_id.images.downsized.url
        img_response = requests.get(image_url, timeout=TIMEOUT)
        file_name = f"{self.sort}-{topic_slug}.gif"
        file_path = os.path.join(self.output_folder, FOLDER_PREFIX, file_name)
        with open(file_path, "wb") as f:
            f.write(img_response.content)
        logger.info('Downloaded %s', file_path)
        return file_path
