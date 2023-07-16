import asyncio
import os
import random
import re
from typing import List

from moviepy.editor import concatenate_videoclips
from slugify import slugify

from generation.audio import Audio
from generation.gifs import Gifs
from generation.images import Images
from generation.video import Video
from services.keywords import Keyword
from utils.common import SettingsLoader
from utils.logs import logger


class Generator:

    APP_NAME = "GENERATOR"

    def __init__(
            self,
            prompt: str,
            script: str,
            fps: int,
            duration: int,
            **kwargs,
        ):
        self.prompt = prompt
        self.script = script
        self.fps = fps
        self.duration = duration
        self.options = SettingsLoader.load(self.APP_NAME, kwargs)
        self.output = os.path.join(
            self.options.get('output_folder'),
            slugify(self.prompt, max_length=30)
        )

    async def _generate_images(self, sections: list):
        # broll = self._extract_broll_list()
        tasks: List[asyncio.Task] = []
        for section in sections:
            tasks.append(
                Images().generate(
                    section,
                    self.output,
                )
            )
        images = await asyncio.gather(*tasks)
        return images

    async def _generate_gifs(self, sections: list):
        # broll = self._extract_broll_list()
        tasks: List[asyncio.Task] = []
        for section in sections:
            tasks.append(
                Gifs().generate(
                    section,
                    self.output
                )
            )
        gifs = await asyncio.gather(*tasks)
        return gifs

    async def _generate_audio(self, sections):
        tasks: List[asyncio.Task] = []
        for section in sections:
            tasks.append(
                Audio().generate(
                    section,
                    self.output,
                )
            )
        audio = await asyncio.gather(*tasks)
        return audio

    async def _generate_video(self, sections: dict,):
        clips = await self._generate_video_clips(sections)
        clips = sorted(clips, key=lambda x: x["index"])
        clips = [clip["clip"] for clip in clips]
        video = concatenate_videoclips(clips, method='compose')
        file_path = os.path.join(self.output, "video.mp4")
        video.write_videofile(file_path)
        return file_path

    async def _generate_video_clips(self, sections: dict):
        count = len(sections)
        tasks: List[asyncio.Task] = []
        for index in range(count):
            tasks.append(
                Video().generate(
                    index,
                    sections[index],
                    self.fps,
                    self.output,
                )
            )
        clips = await asyncio.gather(*tasks)
        return clips

    def _generate_code_block(self,):
        pass

    def _extract_video_sections(self):
        sentences = re.split(r'(?<=[.!?])', self.script.replace('\n', ' '))
        sections = []
        for index, sentence in enumerate(sentences):
            if sentence == '\n' or sentence == '':
                continue
            keywords = Keyword().generate(sentence)
            topic_slug = slugify(','.join(keywords))
            sections.append({
                "index": index,
                "sentence": sentence,
                "keywords": keywords,
                "topic_slug": topic_slug,
                "media": {}
            })
        return sections

    async def generate(self,):
        # Create output folder
        os.makedirs(self.output, exist_ok=True)

        # Save Script into a text file
        with open(os.path.join(self.output, "script.txt"), "w", encoding="utf-8") as f:
            f.write(self.script)

        # Divide sections and get keywords per section
        sections = self._extract_video_sections()
        logger.info("Sections %s", sections)

        gif_sections = []
        image_sections = []
        for section in sections:
            random_list = random.choice([gif_sections,])
            random_list.append(section)

        await asyncio.gather(
            self._generate_images(image_sections),
            self._generate_gifs(gif_sections),
            self._generate_audio(sections),
        )

        video = await self._generate_video(sections)
        return video

    # def _test_images(self, image_sections):
    #     for section in image_sections:
    #         section["media"]["broll_path"] = os.path.join('./output/what-is-artificial-intelligenc/images', f'{section["index"]}-{section["topic_slug"]}.jpg')
    #     return image_sections
    
    # def _test_gifs(self, gif_sections):
    #     for section in gif_sections:
    #         section["media"]["broll_path"] = os.path.join('./output/what-is-artificial-intelligenc/gifs', f'{section["index"]}-{section["topic_slug"]}.mp4')
    #     return gif_sections

    # def _test_audio(self, audio_sections):
    #     for section in audio_sections:
    #         section["media"]["audio_path"] = os.path.join('./output/what-is-artificial-intelligenc/audio', f'{section["index"]}-{section["topic_slug"]}.wav')
    #     return audio_sections
