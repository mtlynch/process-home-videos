import calendar
import collections
import csv
import datetime

import age
import scene as scene_model
import scene_sort
import tags

_FRAME_RATE = 29.970029

_SOURCE_EXTENSION = 'mp4'
_OUTPUT_EXTENSION = 'mp4'


def parse_scene_metadata(scene_metadata_path, configuration):
    raw_scenes = _read_raw_scene_metadata(scene_metadata_path)
    scene_counter = collections.defaultdict(lambda: 1)
    scenes = []
    for i in range(len(raw_scenes)):
        raw_scene = raw_scenes[i]

        title = raw_scene['title']
        if not title or title == 'junk':
            continue

        tape_id = raw_scene['tape_id']
        tape_shortname = raw_scene['tape_shortname']
        tape_friendly_name = raw_scene['tape_friendly_name']

        scene_index = scene_counter[tape_id]
        scene_counter[tape_id] += 1

        scene_date = _get_scene_date(
            raw_scenes, i, configuration['incorrectly_ordered_scenes'])
        scene_tags = _tags_from_metadata(raw_scene, configuration['tags'])

        scene_start_frame = raw_scene['scene_start_frame']
        timecode_start = _frame_number_to_timestamp(scene_start_frame)

        if i == len(raw_scenes) - 1:
            duration_frames = None
        else:
            next_tape_id = raw_scenes[i + 1]['tape_id']
            if tape_id == next_tape_id:
                next_scene_start_frame = raw_scenes[i + 1]['scene_start_frame']
                duration_frames = int(next_scene_start_frame) - int(
                    scene_start_frame)
                if duration_frames <= 0:
                    raise ValueError('Duration can\'t be negative!')
            else:
                duration_frames = None
        description = _full_description(raw_scene['description'], scene_tags,
                                        scene_date, tape_friendly_name,
                                        scene_index, configuration['birthdays'])
        raw_source_filename = tape_id + '.' + _SOURCE_EXTENSION
        rendered_filename = _generate_output_filename(
            _qualified_title(tape_shortname, scene_index, title))
        scenes.append(
            scene_model.SortableScene(raw_source_filename, title, description,
                                      list(scene_tags), timecode_start,
                                      duration_frames, rendered_filename,
                                      scene_index, scene_date))

    return scene_sort.sort(scenes)


def _read_raw_scene_metadata(scene_metadata_path):
    with open(scene_metadata_path) as scene_csv:
        reader = csv.DictReader(scene_csv)
        return [r for r in reader]


def _find_minimum_date(raw_scenes, start_index, tape_id,
                       incorrectly_ordered_scenes):
    i = start_index
    while i >= 0 and raw_scenes[i]['tape_id'] == tape_id:
        raw_scene = raw_scenes[i]
        if raw_scene['date'] and not _is_incorrectly_ordered_scene(
                raw_scene, incorrectly_ordered_scenes):
            return raw_scene['date']
        i -= 1
    raise ValueError('Could not find minimum date')


def _find_maximum_date(raw_scenes, start_index, tape_id,
                       incorrectly_ordered_scenes):
    i = start_index
    while i < len(raw_scenes) and raw_scenes[i]['tape_id'] == tape_id:
        raw_scene = raw_scenes[i]
        if raw_scene['date'] and not _is_incorrectly_ordered_scene(
                raw_scene, incorrectly_ordered_scenes):
            return raw_scene['date']
        i += 1
    raise ValueError('Could not find maximum date')


def _get_scene_date(raw_scenes, i, incorrectly_ordered_scenes):
    current_scene = raw_scenes[i]

    current_scene_year = None
    current_scene_month = None
    current_scene_day = None
    if current_scene['date']:
        current_scene_year, current_scene_month, current_scene_day = _parse_date(
            current_scene['date'])
    if current_scene_day:
        return scene_model.SceneDate(
            exact_date=_parse_exact_date(current_scene['date']))
    else:
        tape_id = current_scene['tape_id']
        return scene_model.SceneDate(date_minimum=_parse_minimum_date(
            _find_minimum_date(raw_scenes, i, tape_id,
                               incorrectly_ordered_scenes)),
                                     date_maximum=_parse_maximum_date(
                                         _find_maximum_date(
                                             raw_scenes, i, tape_id,
                                             incorrectly_ordered_scenes)))


def _frame_number_to_timestamp(frame_number):
    total_seconds = float(frame_number) / _FRAME_RATE
    return str(datetime.timedelta(seconds=total_seconds))


def _tags_from_metadata(scene_metadata, tag_configuration):
    tag_mapper = tags.TagMapper(tag_configuration['keywords'],
                                tag_configuration['mappings'])
    return tags.derive_from_metadata(scene_metadata, tag_mapper)


def _is_incorrectly_ordered_scene(raw_scene, incorrectly_ordered_scenes):
    """Scenes that appear on a tape out of chronological order"""
    return raw_scene['title'] in incorrectly_ordered_scenes


def _parse_date(date_string):
    date_parts = date_string.split('-')
    year = int(date_parts[0])
    if len(date_parts) > 1:
        month = int(date_parts[1])
    else:
        month = None

    if len(date_parts) > 2:
        day = int(date_parts[2])
    else:
        day = None

    return year, month, day


def _parse_minimum_date(date_string):
    year, month, day = _parse_date(date_string)
    if not month:
        month = 1
    if not day:
        day = 1
    return datetime.date(year=year, month=month, day=day)


def _parse_maximum_date(date_string):
    year, month, day = _parse_date(date_string)
    if not month:
        month = 12
    if not day:
        day = calendar.monthrange(year, month)[1]
    return datetime.date(year=year, month=month, day=day)


def _parse_exact_date(date_string):
    year, month, day = _parse_date(date_string)
    return datetime.date(year=year, month=month, day=day)


def _generate_output_filename(qualified_title):
    basename = qualified_title
    bad_characters = [
        '?',
        '\'',
        '"',
        '(',
        ')',
    ]
    for bad_character in bad_characters:
        basename = basename.replace(bad_character, '')

    return '%s.%s' % (basename, _OUTPUT_EXTENSION)


def _qualified_title(tape_shortname, scene_index, title):
    return '%s - %02d - %s' % (tape_shortname, scene_index, title)


def _full_description(description, tags, scene_date, tape_friendly_name,
                      scene_index, birthdays):
    description_parts = []

    if description:
        description_parts.append(description)
    for tag in tags:
        if tag in birthdays:
            age_descriptor = age.derive_age(scene_date, birthdays[tag])
            name = tag[0].upper() + tag[1:]
            description_parts.append('%s is %s.' % (name, age_descriptor))
    description_parts.append('Recorded %s.' % _friendly_date(scene_date))
    description_parts.append('Came from tape "%s," scene #%02d.' %
                             (tape_friendly_name, scene_index))

    return '\n'.join(description_parts)


def _friendly_date(scene_date):
    if scene_date.exact_date:
        return _format_date(scene_date.exact_date)
    else:
        return 'between %s and %s' % (_format_date(
            scene_date.date_minimum), _format_date(scene_date.date_maximum))


def _strip_leading_zeroes(s):
    return s.replace(' 0', ' ')


def _format_date(d):
    return _strip_leading_zeroes(d.strftime('%B %d, %Y'))
