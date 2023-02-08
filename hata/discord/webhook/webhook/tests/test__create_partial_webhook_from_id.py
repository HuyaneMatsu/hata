import vampytest

from ..preinstanced import WebhookType
from ..utils import create_partial_webhook_from_id
from ..webhook import Webhook


def test__create_partial_webhook_from_id__0():
    """
    Tests whether ``create_partial_webhook_from_id`` works as intended.
    
    Case: fields.
    """
    webhook_id = 202302050117
    token = 'nue'
    channel_id = 202302050118
    webhook_type = WebhookType.server
    
    webhook = create_partial_webhook_from_id(webhook_id, token, channel_id = channel_id, webhook_type = webhook_type)
    
    vampytest.assert_instance(webhook, Webhook)
    vampytest.assert_eq(webhook.id, webhook_id)
    vampytest.assert_eq(webhook.token, token)
    vampytest.assert_eq(webhook.channel_id, channel_id)
    vampytest.assert_is(webhook.type, webhook_type)


def test__create_partial_webhook_from_id__1():
    """
    Tests whether ``create_partial_webhook_from_id`` works as intended.
    
    Case: caching.
    """
    webhook_id = 202302050119
    
    webhook = create_partial_webhook_from_id(webhook_id, '')
    test_webhook = create_partial_webhook_from_id(webhook_id, '')
    
    vampytest.assert_is(webhook, test_webhook)
