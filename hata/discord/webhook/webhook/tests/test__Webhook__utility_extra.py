import vampytest

from ..webhook import Webhook


def _iter_options__url():
    yield 202302050115, 'nue', True


@vampytest._(vampytest.call_from(_iter_options__url()).returning_last())
def test__Webhook__url(webhook_id, webhook_token):
    """
    Tests whether ``Webhook.url`` works as intended.
    
    Parameters
    ----------
    webhook_id : `int`
        The webhook's identifier.
    
    webhook_token : `str`
        The webhook's token.
    
    Returns
    -------
    has_url : `bool`
    """
    webhook = Webhook.precreate(
        webhook_id,
        token = webhook_token,
    )
    
    output = webhook.url
    vampytest.assert_instance(output, str)
    return (output is not None)
