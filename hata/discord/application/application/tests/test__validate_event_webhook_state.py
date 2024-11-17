import vampytest

from ..fields import validate_event_webhook_state
from ..preinstanced import ApplicationEventWebhookState


def _iter_options__passing():
    yield None, ApplicationEventWebhookState.none
    yield ApplicationEventWebhookState.disabled, ApplicationEventWebhookState.disabled
    yield ApplicationEventWebhookState.disabled.value, ApplicationEventWebhookState.disabled


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_event_webhook_state(input_value):
    """
    Tests whether ``validate_event_webhook_state`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationEventWebhookState``
        
    Raises
    ------
    TypeError
    """
    output = validate_event_webhook_state(input_value)
    vampytest.assert_instance(output, ApplicationEventWebhookState)
    return output
