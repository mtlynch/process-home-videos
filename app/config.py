import datetime

import yaml


def from_yaml(config_file):
    data = yaml.load(config_file)
    return {
        'birthdays': _parse_birthdays(data['birthdays']),
        'tags': data['tags'],
        'incorrectly_ordered_scenes': data['incorrectly_ordered_scenes'],
    }


def empty():
    return {
        'birthdays': {},
        'tags': {
            'keywords': [],
            'mappings': {},
        }
    }


def _parse_birthdays(birthdays_raw):
    parsed = {}
    for name, birthday_string in birthdays_raw.items():
        parsed[name] = datetime.datetime.strptime(birthday_string,
                                                  '%Y-%m-%d').date()
    return parsed
