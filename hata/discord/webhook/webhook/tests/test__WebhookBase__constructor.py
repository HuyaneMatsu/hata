import vampytest

from ....bases import Icon, IconType

from ..preinstanced import WebhookType
from ..webhook_base import WebhookBase


def _assert_fields_set(webhook):
    """
    Asserts whether every fields of the given webhook are set.
    
    Parameters
    ----------
    webhook : ``WebhookBase``
        The webhook to check.
    """
    vampytest.assert_instance(webhook, WebhookBase)
    vampytest.assert_instance(webhook.avatar, Icon)
    vampytest.assert_instance(webhook.id, int)
    vampytest.assert_instance(webhook.name, str)
    vampytest.assert_instance(webhook.channel_id, int)
    vampytest.assert_instance(webhook.type, WebhookType)


def test__WebhookBase__new__0():
    """
    Tests whether ``WebhookBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    webhook = WebhookBase()
    _assert_fields_set(webhook)


def test__WebhookBase__new__1():
    """
    Tests whether ``WebhookBase.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    name = 'voice in the dark'
    channel_id = 202302050000
    webhook_type = WebhookType.server
    
    webhook = WebhookBase(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
    )
    _assert_fields_set(webhook)
    
    vampytest.assert_eq(webhook.avatar, avatar)
    vampytest.assert_eq(webhook.name, name)
    vampytest.assert_eq(webhook.channel_id, channel_id)
    vampytest.assert_is(webhook.type, webhook_type)


def test__WebhookBase__create_empty():
    """
    Tests whether ``WebhookBase._create_empty`` works as intended.
    """
    webhook_id = 202302050001
    webhook = WebhookBase._create_empty(webhook_id)
    _assert_fields_set(webhook)
    
    vampytest.assert_eq(webhook.id, webhook_id)
