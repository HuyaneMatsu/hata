import vampytest

from ....bases import IconType, Icon

from ..preinstanced import WebhookType
from ..webhook_repr import WebhookRepr

from .test__WebhookBase__constructor import _assert_fields_set


def test__WebhookRepr__from_data():
    """
    Tests whether ``WebhookRepr.from_data`` works as intended.
    """
    webhook_id = 202302050024
    name = 'suika'
    avatar = Icon(IconType.static, 24)
    channel_id = 202302050025
    webhook_type = WebhookType.server
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'username': name,
    }
    
    webhook = WebhookRepr.from_data(data, webhook_id, webhook_type, channel_id)
    vampytest.assert_instance(webhook, WebhookRepr)
    _assert_fields_set(webhook)
    
    vampytest.assert_eq(webhook.avatar, avatar)
    vampytest.assert_eq(webhook.name, name)
    vampytest.assert_eq(webhook.id, webhook_id)
    vampytest.assert_eq(webhook.channel_id, channel_id)
    vampytest.assert_is(webhook.type, webhook_type)
