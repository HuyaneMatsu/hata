import vampytest

from ....scheduled_event import ScheduledEvent

from ..fields import validate_scheduled_events


def _iter_options__passing():
    scheduled_event_id_0 = 202406270010
    scheduled_event_id_1 = 202406270011
    
    scheduled_event_0 = ScheduledEvent.precreate(scheduled_event_id_0)
    scheduled_event_1 = ScheduledEvent.precreate(scheduled_event_id_1)

    yield None, None
    yield [], None
    yield [scheduled_event_0], {scheduled_event_id_0: scheduled_event_0}
    yield (
        [scheduled_event_0, scheduled_event_0],
        {scheduled_event_id_0: scheduled_event_0},
    )
    yield (
        [scheduled_event_1, scheduled_event_0],
        {scheduled_event_id_0: scheduled_event_0, scheduled_event_id_1: scheduled_event_1},
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_scheduled_events(input_value):
    """
    Validates whether ``validate_scheduled_events`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
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
