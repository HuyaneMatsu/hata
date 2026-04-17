import vampytest

from ..flag_meta import _filter_shifts_by_name


def _iter_options():
    yield (
        {
            ('hey', 2, None),
            ('mister', 3, None),
            ('sister', 4, None),
            ('koishi', 3, None),
            ('koishi', 4, None),
            ('satori', 4, None),
            ('satori', 5, None),
        },
        {
            'koishi',
            'satori',
        },
        {
            'koishi': {3, 4},
            'satori': {4, 5},
        }
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__filter_shifts_by_name(accumulated_shifts, duplicates):
    """
    Tests whether ``_filter_shifts_by_name`` works as intended.
    
    Parameters
    ----------
    accumulated_shifts : `set<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    duplicates : `set<str>`
        Duplicated names.
    
    Returns
    -------
    output : `dict<str, set<int>>`
    """
    output = _filter_shifts_by_name(accumulated_shifts, duplicates)
    vampytest.assert_instance(output, dict)
    for key, value in output.items():
        vampytest.assert_instance(key, str)
        vampytest.assert_instance(value, set)
        for element in value:
            vampytest.assert_instance(element, int)
    return output
