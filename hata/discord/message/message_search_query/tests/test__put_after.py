from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_id

from ..fields import put_after


def _iter_options():
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'min_id': 0,
        },
    )
    
    yield (
        after,
        False,
        {
            'min_id': datetime_to_id(after),
        },
    )
    
    yield (
        after,
        True,
        {
            'min_id': datetime_to_id(after),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_after(after, defaults):
    """
    Tests whether ``put_after`` works as intended.
    
    Parameters
    ----------
    after : `None | DateTime`
        Value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_after(after, {}, defaults)
