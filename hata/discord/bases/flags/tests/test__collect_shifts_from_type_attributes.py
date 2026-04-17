from datetime import datetime as DateTime, timezone as TimeZone
import vampytest

from ..flag_deprecation import FlagDeprecation
from ..flag_descriptors import FlagDescriptor
from ..flag_meta import _collect_shifts_from_type_attributes


def _iter_options():
    deprecation = FlagDeprecation(
        'koishi',
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )
    
    yield (
        {},
        (
            set(),
            set(),
        ),
    )
    
    yield (
        {
            'hey': 5,
            'mister': 6,
        },
        (
            set(),
            set(),
        ),
    )
    
    yield (
        {
            'nyan': 4,
            'hey': FlagDescriptor(5),
            'mister': FlagDescriptor(6),
            'sister': FlagDescriptor(7, deprecation = deprecation),
        },
        (
            {
                ('hey', 5, None),
                ('mister', 6, None),
                ('sister', 7, deprecation),
            },
            {
                ('hey', FlagDescriptor(5)),
                ('mister', FlagDescriptor(6)),
                ('sister', FlagDescriptor(7, deprecation = deprecation)),
            },
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__collect_shifts_from_type_attributes(type_attributes):
    """
    Tests whether ``_collect_shifts_from_type_attributes`` works as intended.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    Returns
    -------
    output : `(set<(str, int, None | FlagDeprecation)>,  set<(str, FlagDescriptor)>)`
    """
    accumulated_shifts = set()
    accumulated_flag_descriptors = set()
    
    _collect_shifts_from_type_attributes(
        type_attributes, accumulated_shifts, accumulated_flag_descriptors
    )
    return accumulated_shifts, accumulated_flag_descriptors
