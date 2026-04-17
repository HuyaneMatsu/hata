import vampytest

from ....poll import Poll

from ..fields import validate_poll


def _iter_options__passing():
    poll = Poll(duration = 3600)
    
    yield poll, poll


def _iter_options__type_error():
    yield 12.6
    yield None


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_poll__passing(input_value):
    """
    Tests whether `validate_poll` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : ``Poll``
    
    Raises
    ------
    TypeError
    """
    return validate_poll(input_value)
