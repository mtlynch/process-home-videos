#!/usr/bin/env python3

import argparse
import logging

import mediagoblin
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
    mediagoblin.publish_scenes(read_metadata(args.metadata),
                               args.container_name, args.scenes_dir,
                               args.username,
                               mediagoblin.PublishHistory(args.publish_history))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Publish to MediaGoblin',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'scenes_dir',
        help=
        'Path to processed (output) videos directory within Docker container')
    parser.add_argument('-m',
                        '--metadata',
                        required=True,
                        help='Path to YAML of scene metadata')
    parser.add_argument('-p',
                        '--publish_history',
                        help='Path to MediaGoblin publish history')
    parser.add_argument('-u',
                        '--username',
                        default=u'admin',
                        help='MediaGoblin username to associate with publish')
    parser.add_argument('-c',
                        '--container_name',
                        default='mediagoblin',
                        help='Name of MediaGoblin Docker container')
    main(parser.parse_args())
