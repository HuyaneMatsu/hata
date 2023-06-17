import vampytest

from ....scheduled_event import ScheduledEvent

from ..fields import validate_scheduled_events


def test__validate_scheduled_events__0():
    """
    Tests whether ``validate_scheduled_events`` works as intended.
    
    Case: passing.
    """
    scheduled_event_id = 202306110003
    scheduled_event_name = 'Koishi'
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        name = scheduled_event_name,
    )
    
    for input_value, expected_output in (
        (None, {}),
        ([], {}),
        ({}, {}),
        ([scheduled_event], {scheduled_event_id: scheduled_event}),
        ({scheduled_event_id: scheduled_event}, {scheduled_event_id: scheduled_event}),
    ):
        output = validate_scheduled_events(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_scheduled_events__1():
    """
    Tests whether ``validate_scheduled_events`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_scheduled_events(input_value)
