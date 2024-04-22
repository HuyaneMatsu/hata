from datetime import datetime as DateTime

import vampytest

from ....poll import Poll

from ..fields import validate_poll


def _iter_options__passing():
    poll = Poll(expires_at = DateTime(2016, 5, 14))
    
    yield None, None
    yield poll, poll


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_poll(input_value):
    """
    Tests whether `validate_poll` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        value to validate.
    
    Returns
    -------
    output : `None | Poll`
    
    Raises
    ------
    TypeError
    """
    return validate_poll(input_value)
