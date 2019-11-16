class TagMapper(object):

    def __init__(self, tag_keywords, tag_mappings):
        self._tag_keywords = set(tag_keywords)
        self._tag_mappings = tag_mappings

    def get_tag(self, word):
        normalized_word = word.lower().replace('\'s', '').replace(',', '')
        if normalized_word in self._tag_keywords:
            return normalized_word
        if normalized_word in self._tag_mappings:
            return self._tag_mappings[normalized_word]
        return None


def derive_from_metadata(scene_metadata, tag_mapper):
    tags = set()
    tags |= _tags_from_tag_keys(scene_metadata)
    tags |= _tags_from_string(scene_metadata['other_tags'])
    tags |= _tags_from_title(scene_metadata['title'], tag_mapper)
    return sorted(tags)


def _tags_from_tag_keys(scene_metadata):
    tags = set()
    for k, v in scene_metadata.items():
        # Tag columns start with hash.
        if k.startswith('#') and v:
            tags.add(k[1:])
    return tags


def _tags_from_string(tag_string):
    """Parses tags from a string list of tags.

    Args:
      tag_string: A string list of tags, where each tag is separated by a comma,
        such as:
          'apples, bananas, green grapes'
    
    Returns:
      A set of tags in the string.
    """
    if tag_string:
        return set([t.strip() for t in tag_string.split(',')])
    return set()


def _tags_from_title(title, tag_mapper):
    tags = set()
    for word in title.split():
        tag = tag_mapper.get_tag(word)
        if tag:
            tags.add(tag)
    return tags
