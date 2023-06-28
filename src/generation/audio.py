import os

from elevenlabs import generate, save

from utils.common import SettingsLoader
from utils.logs import logger

FOLDER_PREFIX = "audio/"

class Audio:

    APP_NAME = "ELEVENLABS"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )

    async def generate(self, section: dict, output_folder: str) -> str:
        logger.info('Generating audio for %s', section)
        os.makedirs(os.path.join(output_folder, FOLDER_PREFIX), exist_ok=True)
        audio = generate(
            text=section['sentence'],
            voice=self.options.get("voice"),
            model=self.options.get("model"),
        )
        file_name = f"{section['index']}-{section['topic_slug']}.wav"
        file_path = os.path.join(output_folder, FOLDER_PREFIX, file_name)
        save(audio, file_path)
        logger.info('Downloaded %s', file_path)
        section["audio_path"] = file_path
        return section
