#!/usr/bin/python3

# Converts a user-generated CSV of scene metadata into a YAML string.

import argparse
import logging

import config
import metadata
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


def main(args):
    configure_logging()
    if args.config:
        with open(args.config) as config_file:
            configuration = config.from_yaml(config_file)
    else:
        configuration = config.empty()
    logger.info('Starting to convert CSV file (%s) to YAML', args.metadata)
    print(
        scene_yaml.to_yaml(
            metadata.parse_scene_metadata(args.metadata, configuration)))
    logger.info('Successfully converted CSV (%s) to YAML', args.metadata)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Home Video Processor - Convert CSV to YAML',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', help='Path to config YAML file')
    parser.add_argument('metadata', help='Path to CSV of scene metadata')
    main(parser.parse_args())
