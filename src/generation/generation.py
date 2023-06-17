import copy
import os
import re

from slugify import slugify

from generation.images import Images
from generation.audio import Audio
from generation.video import Video
from generation.summarizer import Summarizer
from generation.gifs import Gifs
from moviepy.editor import concatenate_videoclips
from utils.logs import logger

import glob


OUTPUT_FOLDER = "./output/"

class Generator:
    def __init__(self, prompt, script, fps, duration):
        self.prompt = prompt
        self.script = script
        self.fps = fps
        self.duration = duration
        self.output = os.path.join(OUTPUT_FOLDER, slugify(self.prompt, max_length=30))

    def _generate_broll(self,):
        broll = self._extract_broll_list()
        logger.debug(broll)
        images = []
        index = 0
        for topic in broll:
            image_path = Images(index, topic, self.output).generate()
            images.append(image_path)
            index += 1
        return images

    def _generate_gifs(self,):
        broll = self._extract_broll_list()
        gifs = []
        index = 0
        for topic in broll:
            gif_path = Gifs(index, topic, self.output).generate()
            gifs.append(gif_path)
            index += 1
        return gifs

    def _generate_audio(self,):
        voices = self.__extract_audio_list()
        logger.debug(voices)
        audio = []
        index = 0
        for voice in voices:
            audio_path = Audio(index, voice, self.output).generate()
            audio.append(audio_path)
            index += 1
        return audio

    def __extract_audio_list(self,):
        # broll = re.findall(r'\[.*?\]', self.script)
        # script = copy.copy(self.script)
        # for item in broll:
        #     script = script.replace(item, '')
       
        voices = self.script.split('\n')
        voices_list = []
        for voice in voices:
            if voice == '\n' or voice == '':
                continue
            voice = voice.replace('Host: ', '')
            voice = voice.replace('Guest: ', '')
            voice = voice.replace('Narrator: ', '')
            voice = voice.replace('"', '')
            voice = voice.rstrip()
            voices_list.append(voice)
        return voices_list

    def _generate_video(self, broll, audio, gifs):
        clips = self._generate_video_clips(broll, audio, gifs)
        video = concatenate_videoclips(clips, method='compose')
        file_path = os.path.join(self.output, "video.mp4")
        video.write_videofile(file_path)
        return file_path

    def _generate_video_clips(self, broll, audio, gifs):
        count = len(broll)
        clips = []
        for index in range(count):
            clip = Video(
                index,
                broll[index],
                audio[index],
                gifs[index],
                self.fps,
                self.output,
            ).generate()
            clips.append(clip)
        return clips
        
    def _generate_code_block(self,):
        pass

    def _extract_broll_list(self):
        paragraphs = self.script.split('\n')
        topics = []
        for paragraph in paragraphs:
            if paragraph == '\n' or paragraph == '':
                continue
            sentence = Summarizer(paragraph).generate()
            topics.append(sentence)
        # broll = re.findall(r'\[.*?\]', self.script)
        # topics = []
        # for item in broll:
        #     topics.append(item[1:-1])
        return topics

    def generate(self,):
        # Create output folder
        os.makedirs(self.output, exist_ok=True)

        # Generate broll
        audio = self._generate_audio()
        broll = self._generate_broll()
        gifs = self._generate_gifs()

        video = self._generate_video(broll, audio, gifs)
        return video
        # return True
