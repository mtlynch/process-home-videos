import datetime

import yaml


def from_yaml(config_file):
    data = yaml.safe_load(config_file)
    if not data:
        return empty()
    if 'birthdays' in data and data['birthdays']:
        birthdays = _parse_birthdays(data['birthdays'])
    else:
        birthdays = {}

    if 'tags' in data and data['tags']:
        tags = _parse_tags(data['tags'])
    else:
        tags = {'keywords': [], 'mappings': {}}

    if 'incorrectly_ordered_scenes' in data and data[
            'incorrectly_ordered_scenes']:
        incorrectly_ordered_scenes = _parse_incorrectly_ordered_scenes(
            data['incorrectly_ordered_scenes'])
    else:
        incorrectly_ordered_scenes = []

    return {
        'birthdays': birthdays,
        'tags': tags,
        'incorrectly_ordered_scenes': incorrectly_ordered_scenes,
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
