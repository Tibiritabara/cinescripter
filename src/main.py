import argparse
from utils.logs import logger
from generation.generation import Generator
from generation.script import Script

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        type=str,
        # required=True,
        default="what is machine learning",
        help="Prompt to generate the video"
    )
    parser.add_argument(
        "--tone",
        type=str,
        # required=True,
        default="informative",
        help="Tone of the video"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=24,
        help="FPS of the video"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=10,
        help="Duration of the video"
    )
    return parser.parse_args()


def main():
    logger.info("Initializing video generation ...")
    args = parse_args()
    logger.info("Arguments: %s", args)
    script = Script(args.prompt, args.tone).generate()
    video = Generator(args.prompt, script, args.fps, args.duration).generate()
    return video


if __name__ == "__main__":
    main()
