import os

from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize

from utils.logs import logger

FOLDER_PREFIX = "video/"
TIMEOUT = 30

class Video:
    def __init__(self, sort, image, audio, gif, fps, output_folder):
        self.sort = sort
        self.image = image
        self.audio = audio
        self.gif = gif
        self.fps = fps
        self.output_folder = output_folder

    def generate(self,):
        logger.info('Generating video clip')
        os.makedirs(os.path.join(self.output_folder, FOLDER_PREFIX), exist_ok=True)
        file_name = os.path.basename(self.audio).replace('.wav', '.mp4')
        file_path = os.path.join(self.output_folder, FOLDER_PREFIX, file_name)
        audio_clip = AudioFileClip(self.audio)
        image_clip = ImageClip(self.image)
        image_clip = resize(image_clip, width=1980, height=1080)
        image_clip.duration = (audio_clip.duration / 2)
        gif_clip = VideoFileClip(self.gif)
        gif_clip = resize(gif_clip, width=1980, height=1080)
        gif_clip.duration = (audio_clip.duration / 2)
        video_clip = concatenate_videoclips([image_clip, gif_clip], method='compose')
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.fps = self.fps
        video_clip.write_videofile(file_path)
        logger.info('Stored video clip %s', file_path)
        return video_clip
