import datetime
import unittest

from app import age
from app import scene


class TestAge(unittest.TestCase):

    def test_returns_exact_age_for_on_birthdays(self):
        self.assertEqual(
            '10',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=2000, month=5, day=16)),
                           birthday=datetime.date(year=1990, month=5, day=16)))

    def test_does_not_round_up_ages(self):
        self.assertEqual(
            'almost 10',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=2000, month=5, day=6)),
                           birthday=datetime.date(year=1990, month=5, day=16)))

    def test_reports_a_few_weeks_old(self):
        self.assertEqual(
            'a few weeks old',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=1982, month=12, day=17)),
                           birthday=datetime.date(year=1982, month=11, day=20)))

    def test_reports_half_years_for_ages_under_ten(self):
        self.assertEqual(
            '9-1/2',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=1989, month=7, day=18)),
                           birthday=datetime.date(year=1980, month=1, day=20)))

    def test_stops_reporting_half_years_after_ten(self):
        self.assertEqual(
            '10',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=1990, month=7, day=22)),
                           birthday=datetime.date(year=1980, month=1, day=20)))

    def test_returns_months_for_age_under_two_years(self):
        self.assertEqual(
            '4 months',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=1980, month=5, day=6)),
                           birthday=datetime.date(year=1980, month=1, day=1)))
        self.assertEqual(
            '22 months',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=1981, month=11, day=7)),
                           birthday=datetime.date(year=1980, month=1, day=1)))

    def test_reports_age_when_date_range_does_not_affect_age(self):
        self.assertEqual(
            '5',
            age.derive_age(scene.SceneDate(date_minimum=datetime.date(year=1995,
                                                                      month=2,
                                                                      day=1),
                                           date_maximum=datetime.date(year=1995,
                                                                      month=3,
                                                                      day=25)),
                           birthday=datetime.date(year=1990, month=1, day=1)))
        self.assertEqual(
            '8',
            age.derive_age(scene.SceneDate(date_minimum=datetime.date(year=2008,
                                                                      month=12,
                                                                      day=18),
                                           date_maximum=datetime.date(year=2009,
                                                                      month=1,
                                                                      day=15)),
                           birthday=datetime.date(year=2000, month=11, day=16)))

    def test_reports_newborn_on_exact_date(self):
        self.assertEqual(
            'a newborn',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=2000, month=5, day=6)),
                           birthday=datetime.date(year=2000, month=5, day=6)))

    def test_reports_newborn_thirteen_days_after_birth(self):
        self.assertEqual(
            'a newborn',
            age.derive_age(scene.SceneDate(
                exact_date=datetime.date(year=2000, month=5, day=19)),
                           birthday=datetime.date(year=2000, month=5, day=6)))

    def test_reports_newborn_if_birthday_falls_within_date_range(self):
        self.assertEqual(
            'a newborn',
            age.derive_age(scene.SceneDate(date_minimum=datetime.date(year=2000,
                                                                      month=5,
                                                                      day=1),
                                           date_maximum=datetime.date(year=2000,
                                                                      month=5,
                                                                      day=31)),
                           birthday=datetime.date(year=2000, month=5, day=6)))

    def test_reports_age_in_months_based_on_date_range(self):
        self.assertEqual(
            'between 3 and 5 months',
            age.derive_age(scene.SceneDate(date_minimum=datetime.date(year=2000,
                                                                      month=4,
                                                                      day=1),
                                           date_maximum=datetime.date(year=2000,
                                                                      month=6,
                                                                      day=15)),
                           birthday=datetime.date(year=2000, month=1, day=1)))

    def test_reports_rough_age_based_when_date_range_precedes_birthday(self):
        self.assertEqual(
            'almost 2',
            age.derive_age(scene.SceneDate(date_minimum=datetime.date(year=2002,
                                                                      month=5,
                                                                      day=1),
                                           date_maximum=datetime.date(year=2002,
                                                                      month=5,
                                                                      day=12)),
                           birthday=datetime.date(year=2000, month=5, day=23)))

    def test_reports_rough_age_based_when_date_range_straddles_birthday(self):
        self.assertEqual(
            'around 4',
            age.derive_age(scene.SceneDate(date_minimum=datetime.date(year=2004,
                                                                      month=8,
                                                                      day=1),
                                           date_maximum=datetime.date(year=2004,
                                                                      month=8,
                                                                      day=31)),
                           birthday=datetime.date(year=2000, month=8, day=19)))
