# NOTE: All this date arithmetic is imprecise because it doesn't need to be
# exact.

_SECONDS_PER_YEAR = 31557600.0
_SECONDS_PER_MONTH = _SECONDS_PER_YEAR / 12  # Very imprecise
_SECONDS_PER_DAY = 86400
_REPORT_IN_MONTHS = 23 * _SECONDS_PER_MONTH
_REPORT_HALF_YEARS = 10 * _SECONDS_PER_YEAR
_NEWBORN_THRESHOLD = 14 * _SECONDS_PER_DAY
_SINGLE_MONTH_THRESHOLD = 30 * _SECONDS_PER_DAY


def derive_age(scene_date, birthday):
    if scene_date.exact_date:
        return _derive_exact_age(birthday, scene_date.exact_date)
    return _derive_rough_age(birthday, scene_date.date_minimum,
                             scene_date.date_maximum)


def _derive_exact_age(birthday, exact_date):
    age_in_seconds = _age_in_seconds(birthday, exact_date)
    if age_in_seconds < _NEWBORN_THRESHOLD:
        return 'a newborn'
    if age_in_seconds < _SINGLE_MONTH_THRESHOLD:
        return 'a few weeks old'
    if age_in_seconds < _REPORT_IN_MONTHS:
        return '%d months' % round(age_in_seconds / _SECONDS_PER_MONTH)

    age_in_years = age_in_seconds / _SECONDS_PER_YEAR
    if age_in_years % 1.0 >= 0.75:
        return 'almost %d' % round(age_in_years)

    if age_in_seconds < _REPORT_HALF_YEARS:
        return _format_decimal(
            _round_to_nearest_half(age_in_seconds / _SECONDS_PER_YEAR))

    return str(int(age_in_seconds / _SECONDS_PER_YEAR))


def _derive_rough_age(birthday, date_minimum, date_maximum):
    minimum_age = _derive_exact_age(birthday, date_minimum)
    maximum_age = _derive_exact_age(birthday, date_maximum)
    if minimum_age == 'a newborn':
        return minimum_age
    if 'months' in maximum_age:
        if minimum_age == maximum_age:
            return maximum_age
        else:
            return 'between %s and %s' % (minimum_age.replace(' months',
                                                              ''), maximum_age)
    if minimum_age != maximum_age:
        return 'around %s' % maximum_age.replace('almost ', '').replace(
            'around ', '')
    if _age_in_years(birthday,
                     date_minimum) == _age_in_years(birthday, date_maximum):
        if minimum_age == maximum_age:
            if minimum_age != str(_age_in_years(birthday, date_minimum)):
                return maximum_age
            else:
                return maximum_age
    return 'around %s' % maximum_age


def _age_in_seconds(birthday, exact_date):
    return (exact_date - birthday).total_seconds()


def _age_in_years(birthday, exact_date):
    return int(_age_in_seconds(birthday, exact_date) / _SECONDS_PER_YEAR)


def _round_to_nearest_half(val):
    return round(val * 2.0) / 2.0


def _format_decimal(val):
    return str(val).replace(u'.5', u'-1/2').replace('.0', '')
