from datetime import datetime as DateTime, timedelta as TimeDelta

import vampytest

from ..utils import DATETIME_MAX, DATETIME_MIN, DISCORD_EPOCH_START, id_to_datetime


def _iter_options():
    yield 0, DISCORD_EPOCH_START
    yield  -(1 << 100), DATETIME_MIN
    yield 1 << 100, DATETIME_MAX
    yield (1000 << 22), DISCORD_EPOCH_START + TimeDelta(seconds = 1)
    yield -(1000 << 22), DISCORD_EPOCH_START - TimeDelta(seconds = 1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__id_to_datetime(input_value):
    """
    tests whether ``id_to_datetime`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test with.
    
    Returns
    -------
    output : ``DateTime``
    """
    output = id_to_datetime(input_value)
    vampytest.assert_instance(output, DateTime)
    return output
