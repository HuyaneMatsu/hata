import vampytest

from ....bases import Icon, IconType

from ..preinstanced import WebhookType
from ..webhook_base import WebhookBase


def test__WebhookBase__repr():
    """
    Tests whether ``WebhookBase.__repr__`` works as intended.
    """
    webhook_id = 202302050002
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050003
    webhook_type = WebhookType.server
    
    webhook = WebhookBase._create_empty(webhook_id)
    vampytest.assert_instance(repr(webhook), str)

    webhook = WebhookBase(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
    )
    vampytest.assert_instance(repr(webhook), str)


def test__WebhookBase__hash():
    """
    Tests whether ``WebhookBase.__hash__`` works as intended.
    """
    webhook_id = 202302050004
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050005
    webhook_type = WebhookType.server
    
    webhook = WebhookBase._create_empty(webhook_id)
    vampytest.assert_instance(repr(webhook), str)

    webhook = WebhookBase(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
    )
    vampytest.assert_instance(repr(webhook), str)


def test__WebhookBase__eq():
    """
    Tests whether ``WebhookBase.__eq__`` works as intended.
    """
    webhook_id = 202302050006
    
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050007
    webhook_type = WebhookType.server
    
    keyword_parameters = {
        'avatar': avatar,
        'name': name,
        'channel_id': channel_id,
        'webhook_type': webhook_type,
    }
    
    webhook = WebhookBase(**keyword_parameters)
    vampytest.assert_eq(webhook, webhook)
    vampytest.assert_ne(webhook, object())

    test_webhook = WebhookBase._create_empty(webhook_id)
    vampytest.assert_eq(test_webhook, test_webhook)
    vampytest.assert_ne(webhook, test_webhook)
    
    for field_name, field_value in (
        ('avatar', None),
        ('name', 'okuu'),
        ('channel_id', 0),
        ('webhook_type', WebhookType.bot),
    ):
        test_webhook = WebhookBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(webhook, test_webhook)


def test__WebhookBase__format():
    """
    Tests whether ``WebhookBase.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050008
    webhook_type = WebhookType.server
    
    webhook = WebhookBase(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
    )
    
    vampytest.assert_instance(format(webhook, ''), str)


def test__WebhookBase__sort():
    """
    Tests whether sorting ``WebhookBase` works as intended.
    """
    webhook_id_0 = 202302050009
    webhook_id_1 = 202302050010
    webhook_id_2 = 202302050011
    
    webhook_0 = WebhookBase._create_empty(webhook_id_0)
    webhook_1 = WebhookBase._create_empty(webhook_id_1)
    webhook_2 = WebhookBase._create_empty(webhook_id_2)
    
    to_sort = [
        webhook_1,
        webhook_2,
        webhook_0,
    ]
    
    expected_output = [
        webhook_0,
        webhook_1,
        webhook_2,
    ]
    
    vampytest.assert_eq(sorted(to_sort), expected_output)
