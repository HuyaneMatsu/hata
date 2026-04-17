import vampytest

from ..fields import parse_event_webhook_state
from ..preinstanced import ApplicationEventWebhookState


def _iter_options():
    yield {}, ApplicationEventWebhookState.none
    yield {'event_webhooks_status': ApplicationEventWebhookState.enabled.value}, ApplicationEventWebhookState.enabled


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_event_webhook_state(input_data):
    """
    Tests whether ``parse_event_webhook_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationEventWebhookState``
    """
    output = parse_event_webhook_state(input_data)
    vampytest.assert_instance(output, ApplicationEventWebhookState)
    return output
