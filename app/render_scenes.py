#!/usr/bin/python3

import argparse
import logging

import render
import scene_yaml

logger = logging.getLogger(__name__)


def configure_logging():
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-4s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


def read_metadata(metadata_path):
    with open(metadata_path) as metadata_file:
        return scene_yaml.from_yaml(metadata_file.read())


def main(args):
    configure_logging()
    logger.info('Starting to process scenes')
    render.render_scenes(read_metadata(args.metadata), args.raw_videos_dir,
                         args.output_clips_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Render Scenes',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--metadata',
                        required=True,
                        help='Path to YAML of scene metadata')
    parser.add_argument('--raw_videos_dir',
                        required=True,
                        help='Path to raw (input) videos directory')
    parser.add_argument('--output_clips_dir',
                        required=True,
                        help='Path to processed (output) videos directory')
    main(parser.parse_args())
