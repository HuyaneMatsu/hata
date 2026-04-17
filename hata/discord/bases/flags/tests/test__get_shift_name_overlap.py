import vampytest

from ..flag_meta import _get_shift_name_overlap


def _iter_options():
    yield (
        set(),
        None,
    )
    
    
    yield (
        {
            ('hey', 2, None),
            ('mister', 3, None),
            ('sister', 4, None),
        },
        None,
    )

    yield (
        {
            ('hey', 2, None),
            ('mister', 3, None),
            ('sister', 4, None),
            ('koishi', 3, None),
            ('koishi', 3, None),
        },
        None,
    )

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
        }
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_shift_name_overlap(accumulated_shifts):
    """
    Tests whether ``_get_shift_name_overlap`` works as intended.
    
    Parameters
    ----------
    accumulated_shifts : `list<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    Returns
    -------
    output : `None | set<str>`
    """
    output = _get_shift_name_overlap(accumulated_shifts)
    vampytest.assert_instance(output, set, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    return output
