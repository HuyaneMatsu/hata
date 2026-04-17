import vampytest

from ....poll import Poll

from ...poll_update import PollUpdate

from ..fields import validate_updated


def _iter_options__passing():
    poll = Poll(duration = 3600)
    poll_update = PollUpdate(poll = poll, old_attributes = {'a': 'b'})
    
    yield poll_update, poll_update
    yield None, None


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_updated(input_value):
    """
    Tests whether `validate_updated` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `None | PollUpdate`
    
    Raises
    ------
    TypeError
    """
    return validate_updated(input_value)
