import vampytest

from ....webhook import Webhook

from ..fields import parse_webhooks


def _iter_options():
    webhook_id_0 = 202406240006
    webhook_id_1 = 202406240007
    
    webhook_0 = Webhook.precreate(webhook_id_0)
    webhook_1 = Webhook.precreate(webhook_id_1)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'webhooks': [],
        },
        None,
    )
    
    yield (
        {
            'webhooks': [
                webhook_0.to_data(defaults = True, include_internals = True),
                webhook_1.to_data(defaults = True, include_internals = True),
            ],
        },
        {
            webhook_id_0: webhook_0,
            webhook_id_1: webhook_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_webhooks(input_data):
    """
    Tests whether ``parse_webhooks`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `dict<int, Webhook>`
    """
    return parse_webhooks(input_data)
