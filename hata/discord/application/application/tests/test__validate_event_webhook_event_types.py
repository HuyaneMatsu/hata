import vampytest

from ..fields import validate_event_webhook_event_types
from ..preinstanced import ApplicationEventWebhookEventType


def _iter_options__passing():
    yield (
        None,
        None,
    )
    yield (
        [],
        None,
    )
    yield (
        ApplicationEventWebhookEventType.application_authorization,
        (ApplicationEventWebhookEventType.application_authorization, ),
    )
    yield (
        ApplicationEventWebhookEventType.application_authorization.value,
        (ApplicationEventWebhookEventType.application_authorization, ),
    )
    yield (
        [ApplicationEventWebhookEventType.application_authorization],
        (ApplicationEventWebhookEventType.application_authorization, ),
    )
    yield (
        [ApplicationEventWebhookEventType.application_authorization.value],
        (ApplicationEventWebhookEventType.application_authorization, ),
    )
    yield (
        [
            ApplicationEventWebhookEventType.entitlement_create,
            ApplicationEventWebhookEventType.application_authorization,
        ],
        (
            ApplicationEventWebhookEventType.application_authorization,
            ApplicationEventWebhookEventType.entitlement_create,
        ),
    )
    yield (
        [
            ApplicationEventWebhookEventType.application_authorization,
            ApplicationEventWebhookEventType.entitlement_create,
        ],
        (
            ApplicationEventWebhookEventType.application_authorization,
            ApplicationEventWebhookEventType.entitlement_create,
        ),
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_event_webhook_event_types(input_value):
    """
    Tests whether `validate_event_webhook_event_types` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<ApplicationEventWebhookEventType>`
    
    Raises
    ------
    TypeError
    """
    return validate_event_webhook_event_types(input_value)
