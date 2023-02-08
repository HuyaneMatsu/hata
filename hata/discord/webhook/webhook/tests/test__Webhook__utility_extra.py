import vampytest

from ....utils import is_url

from ..webhook import Webhook


def test__Webhook__url():
    """
    Tests whether ``Webhook.url`` works as intended.
    """
    webhook_id = 202302050115
    token = 'nue'
    
    webhook = Webhook.precreate(
        webhook_id,
        token = token,
    )
    
    output = webhook.url
    vampytest.assert_instance(output, str)
    vampytest.assert_true(is_url(output))
