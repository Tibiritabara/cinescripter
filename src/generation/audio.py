import os

from utils.logs import logger

from elevenlabs import generate, save
from slugify import slugify
from generation.keywords import Keyword

FOLDER_PREFIX = "audio/"
TIMEOUT = 30

class Audio:
    def __init__(self, sort, text, output_folder):
        self.sort = sort
        self.text = text
        self.output_folder = output_folder

    def generate(self,):
        logger.info('Generating audio')
        os.makedirs(os.path.join(self.output_folder, FOLDER_PREFIX), exist_ok=True)
        keyword = Keyword(self.text).generate()
        topic_slug = slugify(keyword)
        audio = generate(
            text=self.text,
            voice=os.getenv("VOICE_ID"),
            model="eleven_monolingual_v1"
        )
        file_name = f"{self.sort}-{topic_slug}.wav"
        file_path = os.path.join(self.output_folder, FOLDER_PREFIX, file_name)
        save(audio, file_path)
        logger.info('Downloaded %s', file_path)
        return file_path
