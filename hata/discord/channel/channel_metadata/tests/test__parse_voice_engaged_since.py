from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_unix_time

from ..fields import parse_voice_engaged_since


def _iter_options():
    voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'voice_start_time': None,
        },
        None,
    )
    
    yield (
        {
            'voice_start_time': datetime_to_unix_time(voice_engaged_since),
        },
        voice_engaged_since,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_voice_engaged_since(input_data):
    """
    Tests whether ``parse_voice_engaged_since`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = parse_voice_engaged_since(input_data)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
