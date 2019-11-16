import datetime

import yaml


def from_yaml(config_file):
    data = yaml.load(config_file)
    if not data:
        return empty()
    return {
        'birthdays':
            _parse_birthdays(data['birthdays']),
        'tags':
            _parse_tags(data['tags']),
        'incorrectly_ordered_scenes':
            _parse_incorrectly_ordered_scenes(data['incorrectly_ordered_scenes']
                                             ),
    }


def empty():
    return {
        'birthdays': {},
        'tags': {
            'keywords': [],
            'mappings': {},
        },
        'incorrectly_ordered_scenes': [],
    }


def _parse_birthdays(birthdays_raw):
    parsed = {}
    if not birthdays_raw:
        return parsed
    for name, birthday_string in birthdays_raw.items():
        parsed[name] = datetime.datetime.strptime(birthday_string,
                                                  '%Y-%m-%d').date()
    return parsed


def _parse_tags(tags):
    if not tags:
        return {
            'keywords': [],
            'mappings': {},
        }
    if 'keywords' in tags and tags['keywords']:
        keywords = tags['keywords']
    else:
        keywords = []

    if 'mappings' in tags and tags['mappings']:
        mappings = tags['mappings']
    else:
        mappings = {}

    return {
        'keywords': keywords,
        'mappings': mappings,
    }


def _parse_incorrectly_ordered_scenes(incorrectly_ordered_scenes):
    if not incorrectly_ordered_scenes:
        return []
    return incorrectly_ordered_scenes
