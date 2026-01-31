from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ....utils import DISCORD_EPOCH_START

from ..fields import validate_after


def _iter_options__passing():
    after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        None
    )
    
    yield (
        after,
        after,
    )
    
    yield (
        DISCORD_EPOCH_START - TimeDelta(days = 30),
        None,
    )
    
    yield (
        DISCORD_EPOCH_START,
        None,
    )


def _iter_options__type_error():
    yield 12.6
    yield '12'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_after(input_value):
    """
    Tests whether `validate_after` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | DateTime`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_after(input_value)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
