import vampytest

from ....webhook import Webhook

from ..fields import put_webhooks


def _iter_options():
    webhook_id_0 = 202406250017
    webhook_id_1 = 202406250018
    
    
    webhook_0 = Webhook.precreate(webhook_id_0)
    webhook_1 = Webhook.precreate(webhook_id_1)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'webhooks': [],
        },
    )
    
    yield (
        {
            webhook_id_0: webhook_0,
            webhook_id_1: webhook_1,
        },
        False,
        {
            'webhooks': [
                webhook_0.to_data(defaults = False, include_internals = True),
                webhook_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        {
            webhook_id_0: webhook_0,
            webhook_id_1: webhook_1,
        },
        True,
        {
            'webhooks': [
                webhook_0.to_data(defaults = True, include_internals = True),
                webhook_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_webhooks(input_value, defaults):
    """
    Tests whether ``put_webhooks`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, Webhook>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_webhooks(input_value, {}, defaults)
