import vampytest

from ..fields import put_event_webhook_state_into
from ..preinstanced import ApplicationEventWebhookState


def _iter_options():
    yield (
        ApplicationEventWebhookState.none,
        False,
        {'event_webhooks_status': ApplicationEventWebhookState.none.value},
    )
    yield (
        ApplicationEventWebhookState.none,
        True,
        {'event_webhooks_status': ApplicationEventWebhookState.none.value},
    )
    
    yield (
        ApplicationEventWebhookState.disabled,
        False,
        {'event_webhooks_status': ApplicationEventWebhookState.disabled.value},
    )
    yield (
        ApplicationEventWebhookState.disabled,
        True,
        {'event_webhooks_status': ApplicationEventWebhookState.disabled.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_event_webhook_state_into(input_value, defaults):
    """
    Tests whether ``put_event_webhook_state_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationEventWebhookState``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_event_webhook_state_into(input_value, {}, defaults)
