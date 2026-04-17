import vampytest

from ....bases import Icon, IconType

from ..preinstanced import WebhookType
from ..webhook_base import WebhookBase

from .test__WebhookBase__constructor import _assert_fields_set


def test__WebhookBase__copy():
    """
    Tests whether ``WebhookBase.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050012
    webhook_type = WebhookType.server
    
    webhook = WebhookBase(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
    )
    
    copy = webhook.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(webhook, copy)
    
    vampytest.assert_eq(webhook, copy)


def test__WebhookBase__copy_with__0():
    """
    Tests whether ``WebhookBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050013
    webhook_type = WebhookType.server
    
    webhook = WebhookBase(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
    )
    
    copy = webhook.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(webhook, copy)
    
    vampytest.assert_eq(webhook, copy)


def test__WebhookBase__copy_with__1():
    """
    Tests whether ``WebhookBase.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 14)
    old_name = 'orin'
    old_channel_id = 202302050014
    old_webhook_type = WebhookType.server
    new_avatar = Icon(IconType.animated, 23)
    new_name = 'okuu'
    new_channel_id = 202302050015
    new_webhook_type = WebhookType.server
    
    webhook = WebhookBase(
        avatar = old_avatar,
        name = old_name,
        channel_id = old_channel_id,
        webhook_type = old_webhook_type,
    )
    
    copy = webhook.copy_with(
        avatar = new_avatar,
        name = new_name,
        channel_id = new_channel_id,
        webhook_type = new_webhook_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(webhook, copy)
    
    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_is(copy.type, new_webhook_type)
