from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_id

from ..fields import put_before


def _iter_options():
    before = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'max_id': 0,
        },
    )
    
    yield (
        before,
        False,
        {
            'max_id': datetime_to_id(before),
        },
    )
    
    yield (
        before,
        True,
        {
            'max_id': datetime_to_id(before),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_before(before, defaults):
    """
    Tests whether ``put_before`` works as intended.
    
    Parameters
    ----------
    before : `None | DateTime`
        Value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_before(before, {}, defaults)
