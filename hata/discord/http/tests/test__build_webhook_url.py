import vampytest

from ...utils import is_url

from ..urls import API_ENDPOINT, build_webhook_url


def _iter_options():
    webhook_id = 202504170020
    webhook_token = 'tewi' * 15
    yield (
        webhook_id,
        webhook_token,
        f'{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_webhook_url(webhook_id, webhook_token):
    """
    Tests whether ``build_webhook_url`` works as intended.
    
    Parameters
    ----------
    webhook_id : `int`
        Webhook identifier.
    
    webhook_token : `str`
        Token to create the webhook with.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_webhook_url(webhook_id, webhook_token)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
