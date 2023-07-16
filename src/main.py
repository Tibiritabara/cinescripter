import argparse
import asyncio

from generation.generation import Generator
from generation.script import Script
from utils.logs import logger


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
    parser.add_argument(
        "--use-db",
        type=bool,
        default=False,
        help="Use database to retrieve the context of the video"
    )
    return parser.parse_args()


async def main():
    logger.info("Initializing video generation ...")
    args = parse_args()
    logger.info("Arguments: %s", args)
    context = ""
    if args.use_db:
        context = Script().get_context(args.prompt)
    script = Script().get_script(context, args.prompt, args.tone)
    logger.info("Script: %s", script)
    video = await Generator(args.prompt, script, args.fps, args.duration).generate()
    return video


if __name__ == "__main__":
    asyncio.run(main())
