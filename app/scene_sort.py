import functools


def sort(scenes):
    return sorted(scenes, key=functools.cmp_to_key(_compare_scenes))


def _compare_scenes(a, b):
    result = _compare_exact_scene_dates(a.scene_date, b.scene_date)
    if result:
        return result
    result = _compare_indices(a, b)
    if result:
        return result
    result = _compare_rough_scene_dates(a.scene_date, b.scene_date)
    if result:
        return result
    return _compare_strings(a.title, b.title)


def _compare_strings(a, b):
    if a == b:
        return 0
    elif a < b:
        return -1
    else:
        return 1


def _compare_dates(a, b):
    return int((a - b).total_seconds())


def _compare_exact_scene_dates(a, b):
    if a.exact_date and b.exact_date:
        return _compare_dates(a.exact_date, b.exact_date)
    else:
        return 0


def _compare_rough_scene_dates(a, b):
    if a.exact_date and b.exact_date:
        return _compare_dates(a.exact_date, b.exact_date)
    elif a.exact_date:
        return _compare_dates(a.exact_date, b.date_minimum)
    elif b.exact_date:
        return _compare_dates(a.date_minimum, b.exact_date)
    else:
        return _compare_dates(a.date_minimum, b.date_minimum)


def _compare_indices(a, b):
    if a.raw_source_filename != b.raw_source_filename:
        return 0
    else:
        return a.scene_index - b.scene_index
