import logging
import os

import docker

logger = logging.getLogger(__name__)


def publish_scenes(scenes, container_name, scenes_dir, publisher_username,
                   publish_history):
    for scene in scenes:
        if publish_history.is_published(scene.rendered_filename):
            logger.info('%s is already published, skipping',
                        scene.rendered_filename)
            continue
        _publish_scene(scene, container_name, scenes_dir, publisher_username,
                       publish_history)


def _publish_scene(scene, container_name, scenes_dir, publisher_username,
                   publish_history):
    _docker_publish(container_name, scenes_dir, publisher_username,
                    scene.rendered_filename, scene.title, scene.description,
                    scene.tags)
    publish_history.add_to_history(scene.rendered_filename)


def _docker_publish(container_name, scenes_dir, publisher_username, file_path,
                    title, description, tags):
    logger.info('Publishing "%s" to docker container %s', file_path,
                container_name)
    client = docker.from_env()
    container = client.containers.get(container_name)
    rc, output = container.exec_run(cmd=[
        'bin/gmg', 'addmedia', publisher_username,
        os.path.join(scenes_dir, file_path), '--title', title, '--description',
        description, '--tags', ','.join(tags)
    ])
    if rc:
        raise ValueError('Docker command failed with exit code %s: %s' %
                         (rc, output))


class PublishHistory(object):

    def __init__(self, publish_history_path):
        self._publish_history_path = publish_history_path
        self._published_files = _read_publish_history(publish_history_path)

    def add_to_history(self, filename):
        self._published_files.add(filename)
        with open(self._publish_history_path, 'a') as publish_history_file:
            publish_history_file.write('%s\n' % filename)

    def is_published(self, filename):
        return filename in self._published_files


def _read_publish_history(publish_history_path):
    if not os.path.exists(publish_history_path):
        return set()
    with open(publish_history_path) as publish_history_file:
        return set([line.strip() for line in publish_history_file.readlines()])
