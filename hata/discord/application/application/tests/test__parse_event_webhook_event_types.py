import vampytest

from ..fields import parse_event_webhook_event_types
from ..preinstanced import ApplicationEventWebhookEventType


def _iter_options():
    yield (
        {},
        None,
    )
    yield (
        {
            'event_webhooks_types': None,
        },
        None,
    )
    yield (
        {
            'event_webhooks_types': [],
        },
        None,
    )
    yield (
        {
            'event_webhooks_types': [
                ApplicationEventWebhookEventType.application_authorization.value,
                ApplicationEventWebhookEventType.entitlement_create.value,
            ],
        },
        (
            ApplicationEventWebhookEventType.application_authorization,
            ApplicationEventWebhookEventType.entitlement_create,
        ),
    )
    yield (
        {
            'event_webhooks_types': [
                ApplicationEventWebhookEventType.entitlement_create.value,
                ApplicationEventWebhookEventType.application_authorization.value,
            ],
        },
        (
            ApplicationEventWebhookEventType.application_authorization,
            ApplicationEventWebhookEventType.entitlement_create,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_event_webhook_event_types(input_data):
    """
    Tests whether ``parse_event_webhook_event_types`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<ApplicationEventWebhookEventType>`
    """
    return parse_event_webhook_event_types(input_data)
