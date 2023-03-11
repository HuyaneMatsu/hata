import vampytest

from ...scheduled_event import ScheduledEvent

from ..fields import validate_scheduled_event_id


@vampytest.skip_if(not hasattr(ScheduledEvent, 'precreate'))
def test__validate_scheduled_event_id__0():
    """
    Tests whether `validate_scheduled_event_id` works as intended.
    
    Case: passing.
    """
    scheduled_event_id = 202303110011
    
    for input_value, expected_output in (
        (None, 0),
        (scheduled_event_id, scheduled_event_id),
        (ScheduledEvent.precreate(scheduled_event_id), scheduled_event_id),
        (str(scheduled_event_id), scheduled_event_id)
    ):
        output = validate_scheduled_event_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_scheduled_event_id__1():
    """
    Tests whether `validate_scheduled_event_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_scheduled_event_id(input_value)


def test__validate_scheduled_event_id__2():
    """
    Tests whether `validate_scheduled_event_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_scheduled_event_id(input_value)
