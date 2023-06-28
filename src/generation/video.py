import os
import pathlib

import moviepy
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip
from moviepy.video.fx.resize import resize

from utils.common import SettingsLoader
from utils.logs import logger

FOLDER_PREFIX = "video/"
TIMEOUT = 30

class Video:

    APP_NAME = "VIDEO"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs,
        )

    async def generate(
            self,
            sort: int,
            media: dict,
            audio: dict,
            fps: int,
            output_folder: str,
    ):
        logger.info('Generating video clip')
        os.makedirs(os.path.join(output_folder, FOLDER_PREFIX), exist_ok=True)

        # AudioFileClip with generated voice
        audio_clip = AudioFileClip(audio["audio_path"])
        clip_duration = audio_clip.duration
        extension = pathlib.Path(media["media_path"]).suffix
        if extension == ".jpg":
            clip = ImageClip(media["media_path"])
        else:
            clip = VideoFileClip(media["media_path"])
            clip_duration = clip.duration
        clip = resize(
            clip,
            width=self.options.get("width", 1920),
            height=self.options.get("height", 1080),
        )
        if extension != ".jpg":
            clip = clip.loop(duration=clip_duration)
        clip = clip.set_audio(audio_clip)
        clip.duration = audio_clip.duration
        clip.fps = fps

        file_name = f"{audio['index']}-{audio['topic_slug']}.mp4"
        file_path = os.path.join(output_folder, FOLDER_PREFIX, file_name)
        clip.write_videofile(file_path)
        logger.info('Stored video clip %s', file_path)
        return {
            "index": sort,
            "clip": clip,
        }
