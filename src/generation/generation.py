import asyncio
import os
import random
from typing import Dict, List

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

    async def _generate_video(self, media: dict, audio: dict):
        clips = await self._generate_video_clips(media, audio)
        clips = sorted(clips, key=lambda x: x["index"])
        clips = [clip["clip"] for clip in clips]
        video = concatenate_videoclips(clips, method='compose')
        file_path = os.path.join(self.output, "video.mp4")
        video.write_videofile(file_path)
        return file_path

    async def _generate_video_clips(self, media: dict, audio: dict):
        count = len(media)
        tasks: List[asyncio.Task] = []
        for index in range(count):
            tasks.append(
                Video().generate(
                    index,
                    media[index],
                    audio[index],
                    self.fps,
                    self.output,
                )
            )
        clips = await asyncio.gather(*tasks)
        return clips

    def _generate_code_block(self,):
        pass

    def _extract_video_sections(self):
        sentences = self.script.replace('\n', '').split('.')
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
            })
        return sections

    async def generate(self,):
        # Create output folder
        os.makedirs(self.output, exist_ok=True)
        sections = self._extract_video_sections()
        logger.info("Sections %s", sections)

        gif_sections = []
        image_sections = []
        for section in sections:
            random_list = random.choice([gif_sections, image_sections])
            random_list.append(section)

        images, gifs, audio = await asyncio.gather(
            self._generate_images(image_sections),
            self._generate_gifs(gif_sections),
            self._generate_audio(sections),
        )
        # images, gifs, audio = self.test_files()

        media = sorted(images + gifs, key=lambda x: x["index"])

        video = await self._generate_video(media, audio)
        return video
        # return True

    # def test_files(self,):
    #     image_paths = next(os.walk('./output/what-is-artificial-intelligenc/images'), (None, None, []))[2]
    #     images = []
    #     for image in image_paths:
    #         if image == '.DS_Store':
    #             continue
    #         images.append({
    #             "index": int(os.path.basename(image).split('-')[0]),
    #             "topic_slug": "-".join(os.path.basename(image).split('-')[1:]).replace(".jpg", ""),
    #             "file_path": os.path.join('./output/what-is-artificial-intelligenc/images', image),
    #         })
    #     images = sorted(images, key=lambda x: x["index"])

    #     gif_paths = next(os.walk('./output/what-is-artificial-intelligenc/gifs'), (None, None, []))[2]
    #     gifs = []
    #     for gif in gif_paths:
    #         if gif == '.DS_Store':
    #             continue
    #         gifs.append({
    #             "index": int(os.path.basename(gif).split('-')[0]),
    #             "topic_slug": "-".join(os.path.basename(gif).split('-')[1:]).replace(".mp4", ""),
    #             "file_path": os.path.join('./output/what-is-artificial-intelligenc/gifs', gif)
    #         })
    #     gifs = sorted(gifs, key=lambda x: x["index"])

    #     audio_paths = next(os.walk('./output/what-is-artificial-intelligenc/audio'), (None, None, []))[2]
    #     audios = []
    #     for audio in audio_paths:
    #         if audio == '.DS_Store':
    #             continue
    #         audios.append({
    #             "index": int(os.path.basename(audio).split('-')[0]),
    #             "topic_slug": "-".join(os.path.basename(audio).split('-')[1:]).replace(".wav", ""),
    #             "file_path": os.path.join('./output/what-is-artificial-intelligenc/audio', audio),
    #         })
    #     audios = sorted(audios, key=lambda x: x["index"])

    #     return images, gifs, audios
