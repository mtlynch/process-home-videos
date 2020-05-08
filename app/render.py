import logging
import os
import re
import subprocess
import tempfile

_FFMPEG_CMD_TEMPLATE = """
ffmpeg
    -y
    -ss {timecode_start}
    -i "{raw_file_path}"
    -c:v libx264
    -crf 22
    -preset veryslow
    -tune grain
    -c:a aac
    -b:a 128k
    {frame_arg}
    "{output_path}"
"""

logger = logging.getLogger(__name__)


def render_scenes(scenes, input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for scene in scenes:
        _render_scene(scene, input_dir, output_dir)


def _render_scene(scene, input_dir, output_dir):
    raw_file_path = os.path.join(input_dir, scene.raw_source_filename)
    output_path = os.path.join(output_dir, scene.rendered_filename)
    if os.path.exists(output_path):
        logger.info('%s already exists, skipping', scene.rendered_filename)
        return

    intermediate_output_path = _generate_intermediate_output_path(
        output_dir, scene.rendered_filename)

    render_with_ffmpeg(raw_file_path, scene.timecode_start,
                       scene.duration_frames, intermediate_output_path)

    os.rename(intermediate_output_path, output_path)


def _generate_intermediate_output_path(output_dir, rendered_filename):
    output_extension = os.path.splitext(rendered_filename)[1]
    intermediate_output_filename = rendered_filename.replace(
        output_extension, '-tmpfile' + output_extension)
    return os.path.join(output_dir, intermediate_output_filename)


def render_with_ffmpeg(raw_file_path, timecode_start, duration_frames,
                       output_path):
    render_command = _generate_render_command(raw_file_path, timecode_start,
                                              duration_frames, output_path)
    logger.info('Rendering %s\n%s\n\n', os.path.basename(raw_file_path),
                render_command)

    with tempfile.TemporaryFile() as output_buffer:
        try:

            subprocess.check_call(render_command,
                                  stderr=output_buffer,
                                  shell=True)
        except subprocess.CalledProcessError as e:
            logger.error('Failed: %s', e)
            output_buffer.seek(0)
            logger.error(output_buffer.read().decode('utf-8'))
            raise


def _generate_render_command(raw_file_path, timecode_start, duration_frames,
                             output_path):
    if duration_frames:
        frame_arg = '-frames:v %d' % duration_frames
    else:
        frame_arg = ''
    return _format_shell_command(_FFMPEG_CMD_TEMPLATE).format(
        raw_file_path=raw_file_path,
        timecode_start=timecode_start,
        frame_arg=frame_arg,
        output_path=output_path)


def _format_shell_command(command):
    formatted_command = command.strip().replace('\r', '').replace('\n', '')
    return re.sub('\s+', ' ', formatted_command)
