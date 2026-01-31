from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ....utils import DISCORD_EPOCH_START

from ..fields import validate_before


def _iter_options__passing():
    before = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        None
    )
    
    yield (
        before,
        before,
    )
    
    yield (
        DISCORD_EPOCH_START - TimeDelta(days = 30),
        DISCORD_EPOCH_START,
    )
    
    yield (
        DISCORD_EPOCH_START,
        DISCORD_EPOCH_START,
    )


def _iter_options__type_error():
    yield 12.6
    yield '12'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_before(input_value):
    """
    Tests whether `validate_before` works as intended.
    
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
    output = validate_before(input_value)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
