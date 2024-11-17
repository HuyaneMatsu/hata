from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flag_deprecation import FlagDeprecation
from ..flag_meta import _build_shifts


def _iter_options():
    deprecation = FlagDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    yield (
        {
            ('hey', 0, None),
            ('mister', 0, None),
            ('sister', 1, None),
        },
        (
            {
                'hey': 0,
                'mister': 0,
                'sister': 1,
            },
            {},
        ),
    )
    
    yield (
        {
            ('hey', 0, None),
            ('mister', 0, deprecation),
            ('sister', 1, deprecation),
        },
        (
            {
                'hey': 0,
            },
            {
                'mister': (0, deprecation),
                'sister': (1, deprecation),
            },
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_shifts(accumulated_reverse_descriptors):
    """
    Tests whether ``_build_shifts`` works as intended.
    
    Parameters
    ----------
    accumulated_shifts : `set<(str, int, None | FlagDeprecation)>`
        The accumulated shifts by their name.
    
    Returns
    -------
    output : `(dict<str, int>, dict<str, (int, FlagDeprecation)>`
    """
    output = _build_shifts(accumulated_reverse_descriptors)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    shifts, deprecated_shifts = output
    
    vampytest.assert_instance(shifts, dict)
    for key, value in shifts.items():
        vampytest.assert_instance(key, str)
        vampytest.assert_instance(value, int)
    
    vampytest.assert_instance(deprecated_shifts, dict)
    for key, value in deprecated_shifts.items():
        vampytest.assert_instance(key, str)
        vampytest.assert_instance(value, tuple)
        vampytest.assert_eq(len(value), 2)
        vampytest.assert_instance(value[0], int)
        vampytest.assert_instance(value[1], FlagDeprecation)
    
    return output
