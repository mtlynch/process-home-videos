import unittest

from app import tags


class TestTagMapper(unittest.TestCase):

    def test_recognizes_exact_keyword(self):
        mapper = tags.TagMapper(tag_keywords=['candy', 'fish'], tag_mappings={})
        self.assertEqual('fish', mapper.get_tag('fish'))

    def test_recognizes_keyword_with_different_casing(self):
        mapper = tags.TagMapper(tag_keywords=['candy', 'fish'], tag_mappings={})
        self.assertEqual('fish', mapper.get_tag('FiSH'))

    def test_recognizes_keyword_with_apostrophe_s(self):
        mapper = tags.TagMapper(tag_keywords=['dave', 'fish'], tag_mappings={})
        self.assertEqual('dave', mapper.get_tag('dave\'s'))

    def test_recognizes_keyword_with_trailing_comma(self):
        mapper = tags.TagMapper(tag_keywords=['dave', 'fish'], tag_mappings={})
        self.assertEqual('dave', mapper.get_tag('dave,'))

    def test_recognizes_mapped_keyword(self):
        mapper = tags.TagMapper(tag_keywords=[],
                                tag_mappings={'bill': 'bill gates'})
        self.assertEqual('bill gates', mapper.get_tag('bill'))


class TestDeriveFromMetadata(unittest.TestCase):

    def test_derives_tags_from_tag_keys(self):
        self.assertEqual(['alice', 'bob', 'catherine'],
                         tags.derive_from_metadata(
                             {
                                 'tape_id': 'dummy-tape-id-1',
                                 'title': 'Dummy Scene Title',
                                 '#bob': 'y',
                                 '#alice': 'y',
                                 '#catherine': 'y',
                                 'other_tags': '',
                             }, tags.TagMapper([], {})))

    def test_derives_tags_from_other_tags_key(self):
        self.assertEqual(['best of', 'birthdays', 'kittens'],
                         tags.derive_from_metadata(
                             {
                                 'tape_id': 'dummy-tape-id-1',
                                 'title': 'Dummy Scene Title',
                                 '#bob': '',
                                 '#alice': '',
                                 '#catherine': '',
                                 'other_tags': 'kittens, birthdays, best of',
                             }, tags.TagMapper([], {})))

    def test_derives_tags_from_title(self):
        self.assertEqual(['abby wanderhouse', 'dave'],
                         tags.derive_from_metadata(
                             {
                                 'tape_id': 'dummy-tape-id-1',
                                 'title': 'Dave Gives Abby a Prseent',
                                 '#bob': '',
                                 '#alice': '',
                                 '#catherine': '',
                                 'other_tags': '',
                             },
                             tags.TagMapper(
                                 tag_keywords=['dave'],
                                 tag_mappings={'abby': 'abby wanderhouse'})))

    def test_derives_tags_from_all_sources(self):
        self.assertEqual(
            ['abby wanderhouse', 'alice', 'best of', 'dave', 'hats'],
            tags.derive_from_metadata(
                {
                    'tape_id': 'dummy-tape-id-1',
                    'title': 'Dave Gives Abby a Prseent',
                    '#bob': '',
                    '#alice': 'y',
                    '#catherine': '',
                    'other_tags': 'best of, hats',
                },
                tags.TagMapper(tag_keywords=['dave'],
                               tag_mappings={'abby': 'abby wanderhouse'})))
