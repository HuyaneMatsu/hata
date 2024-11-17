from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..flag_deprecation import FlagDeprecation
from ..flag_meta import _collect_shifts_from_type_parents


FLAG_DEPRECATION = FlagDeprecation(
    'koishi',
    DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
)

class _TestMeta(type):
    pass


class _TestType0(metaclass = _TestMeta):
    __slots__ = ()
    
    __shifts__ = {
        'hey': 1,
        'mister': 2,
        'sister': 3,
    }
    
    __deprecated_shifts__ = {}


class _TestType1(metaclass = _TestMeta):
    __slots__ = ()
    
    __shifts__ = {
        'hello': 3,
        'sister': 4,
    }
    
    __deprecated_shifts__ = {
        'hell_cat': (5, FLAG_DEPRECATION),
    }


class _TestType2(metaclass = type):
    __slots__ = ()
    
    __shifts__ = {
        'hello': 5,
        'hell': 6,
    }
    
    __deprecated_shifts__ = {}



def _iter_options():
    yield (
        _TestMeta,
        (int,),
        set(),
    )
    
    yield (
        _TestMeta,
        (_TestType0,),
        {
            ('hey', 1, None),
            ('mister', 2, None),
            ('sister', 3, None),
        },
    )
    
    yield (
        _TestMeta,
        (int, _TestType2),
        set(),
    )
    
    yield (
        _TestMeta,
        (_TestType0, _TestType1),
        {
            ('hey', 1, None),
            ('mister', 2, None),
            ('sister', 3, None),
            ('hello', 3, None),
            ('sister', 4, None),
            ('hell_cat', 5, FLAG_DEPRECATION),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__collect_shifts_from_type_parents(meta_type, type_parents):
    """
    Tests whether ``_collect_shifts_from_type_parents`` works as intended.
    
    Parameters
    ----------
    meta_type : `type`
        The meta type to allow its children to be collected from.
    
    type_parents : `tuple<type>`
        The parent types.
    
    Returns
    -------
    output : `set<(str, int, None | FlagDeprecation)>`
    """
    accumulated_shifts = set()
    _collect_shifts_from_type_parents(meta_type, type_parents, accumulated_shifts)
    return accumulated_shifts
