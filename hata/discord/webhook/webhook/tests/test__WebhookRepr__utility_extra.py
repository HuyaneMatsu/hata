import vampytest

from ..preinstanced import WebhookType
from ..webhook import Webhook
from ..webhook_repr import WebhookRepr


def test__WebhookRepr__webhook():
    """
    Tests whether ``WebhookRepr.webhook`` works as intended.
    """
    webhook_id = 202302050026
    channel_id = 202302050027
    webhook_type = WebhookType.server
    
    webhook_repr = WebhookRepr()
    webhook_repr.id = webhook_id
    webhook_repr.type = webhook_type
    webhook_repr.channel_id = channel_id
    
    webhook = webhook_repr.webhook
    vampytest.assert_instance(webhook, Webhook)
    vampytest.assert_eq(webhook.id, webhook_id)
    vampytest.assert_is(webhook.type, webhook_type)
    vampytest.assert_eq(webhook.channel_id, channel_id)
    
    # Check caching too
    test_webhook = webhook_repr.webhook
    vampytest.assert_is(webhook, test_webhook)
