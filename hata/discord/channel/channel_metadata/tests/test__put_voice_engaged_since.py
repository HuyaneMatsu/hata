from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_unix_time

from ..fields import put_voice_engaged_since


def _iter_options():
    voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'voice_start_time': None,
        },
    )
    
    yield (
        voice_engaged_since,
        False,
        {
            'voice_start_time': datetime_to_unix_time(voice_engaged_since),
        },
    )
    
    yield (
        voice_engaged_since,
        True,
        {
            'voice_start_time': datetime_to_unix_time(voice_engaged_since),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_voice_engaged_since(input_value, defaults):
    """
    Tests whether ``put_voice_engaged_since`` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_voice_engaged_since(input_value, {}, defaults)
