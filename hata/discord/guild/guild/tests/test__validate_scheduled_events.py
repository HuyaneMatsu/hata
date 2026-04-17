import vampytest

from ....scheduled_event import ScheduledEvent

from ..fields import validate_scheduled_events


def _iter_options__passing():
    scheduled_event_id = 202306110003
    scheduled_event_name = 'Koishi'
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        name = scheduled_event_name,
    )

    yield None, None
    yield [], None
    yield {}, None
    yield [scheduled_event], {scheduled_event_id: scheduled_event}
    yield {scheduled_event_id: scheduled_event}, {scheduled_event_id: scheduled_event}


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {12.6}
    
    
@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_scheduled_events(input_value):
    """
    Tests whether ``validate_scheduled_events`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<int, ScheduledEvent>`
    
    Raises
    ------
    TypeError
    """
    output = validate_scheduled_events(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
