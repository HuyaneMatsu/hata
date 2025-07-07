import vampytest

from ....scheduled_event import ScheduledEvent

from ..fields import validate_scheduled_event_id


def _iter_options__passing():
    scheduled_event_id = 202303110011
    
    yield None, 0
    yield 0, 0
    yield scheduled_event_id, scheduled_event_id
    yield ScheduledEvent.precreate(scheduled_event_id), scheduled_event_id
    yield str(scheduled_event_id), scheduled_event_id


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield '1111111111111111111111'
    yield -1
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_scheduled_event_id(input_value):
    """
    Tests whether `validate_scheduled_event_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_scheduled_event_id(input_value)
    vampytest.assert_instance(output, int)
    return output
