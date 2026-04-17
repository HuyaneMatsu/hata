import vampytest

from ..fields import put_event_webhook_event_types
from ..preinstanced import ApplicationEventWebhookEventType


def _iter_options():
    yield (
        None,
        False,
        {
            'event_webhooks_types': [],
        },
    )
    yield (
        None,
        True,
        {
            'event_webhooks_types': [],
        },
    )
    yield (
        (
            ApplicationEventWebhookEventType.application_authorization,
            ApplicationEventWebhookEventType.entitlement_create,
        ),
        False,
        {
            'event_webhooks_types': [
                ApplicationEventWebhookEventType.application_authorization.value,
                ApplicationEventWebhookEventType.entitlement_create.value,
            ],
        },
    )
    yield (
        (
            ApplicationEventWebhookEventType.application_authorization,
            ApplicationEventWebhookEventType.entitlement_create,
        ),
        True,
        {
            'event_webhooks_types': [
                ApplicationEventWebhookEventType.application_authorization.value,
                ApplicationEventWebhookEventType.entitlement_create.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_event_webhook_event_types(input_value, defaults):
    """
    Tests whether ``put_event_webhook_event_types`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<ApplicationEventWebhookEventType>`
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_event_webhook_event_types(input_value, {}, defaults)
