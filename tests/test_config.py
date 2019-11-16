import datetime
import io
import unittest

from app import config


class TestConfigFromYaml(unittest.TestCase):

    def test_parses_yaml(self):
        self.assertEqual(
            {
                'birthdays': {
                    'alice': datetime.date(year=2000, month=1, day=1),
                    'bob': datetime.date(year=2001, month=5, day=16),
                    'charlie': datetime.date(year=2002, month=2, day=3),
                },
                'tags': {
                    'keywords': [
                        'alice',
                        'bob',
                        'charlie',
                        'david',
                    ],
                    'mappings': {
                        'alan': 'alan turing',
                        'grace': 'grace hopper',
                    }
                },
                'incorrectly_ordered_scenes': [
                    'Alan Crosses Finish Line',
                    'Charlie Bites My Finger',
                ]
            },
            config.from_yaml(
                io.StringIO("""
      birthdays:
        alice: '2000-01-01'
        bob: '2001-05-16'
        charlie: '2002-02-03'
      tags:
        keywords:
          - alice
          - bob
          - charlie
          - david
        mappings:
          alan: alan turing
          grace: grace hopper
      incorrectly_ordered_scenes:
        - Alan Crosses Finish Line
        - Charlie Bites My Finger
      """)))
