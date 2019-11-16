import yaml

import scene


def to_yaml(scenes):
    return yaml.dump([_scene_to_dict(s) for s in scenes])


def from_yaml(yaml_data):
    scene_dicts = yaml.load(yaml_data)
    return [_dict_to_scene(d) for d in scene_dicts]


def _scene_to_dict(scene):
    return {
        'description': scene.description,
        'title': scene.title,
        'tags': scene.tags,
        'timecode_start': scene.timecode_start,
        'duration_frames': scene.duration_frames,
        'raw_source_filename': scene.raw_source_filename,
        'rendered_filename': scene.rendered_filename,
    }


def _dict_to_scene(scene_dict):
    return scene.Scene(scene_dict['raw_source_filename'], scene_dict['title'],
                       scene_dict['description'], scene_dict['tags'],
                       scene_dict['timecode_start'],
                       scene_dict['duration_frames'],
                       scene_dict['rendered_filename'])
