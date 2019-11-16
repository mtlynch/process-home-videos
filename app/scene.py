class Scene(object):

    def __init__(self, raw_source_filename, title, description, tags,
                 timecode_start, duration_frames, rendered_filename):
        self.raw_source_filename = raw_source_filename

        self.title = title
        self.description = description
        self.tags = tags
        self.timecode_start = timecode_start
        self.duration_frames = duration_frames
        self.rendered_filename = rendered_filename


class SortableScene(Scene):

    def __init__(self, raw_source_filename, title, description, tags,
                 timecode_start, duration_frames, rendered_filename,
                 scene_index, scene_date):
        super().__init__(raw_source_filename, title, description, tags,
                         timecode_start, duration_frames, rendered_filename)
        self.scene_index = scene_index
        self.scene_date = scene_date


class SceneDate(object):

    def __init__(self, exact_date=None, date_minimum=None, date_maximum=None):
        self.exact_date = exact_date
        self.date_minimum = date_minimum
        self.date_maximum = date_maximum
