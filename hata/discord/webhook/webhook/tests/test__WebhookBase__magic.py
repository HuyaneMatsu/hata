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


def test__WebhookBase__eq__non_partial_and_different_object():
    """
    Tests whether ``WebhookBase.__eq__`` works as intended.
    
    Case: non partial and non user object.
    """
    user_id = 202504260015
    
    name = 'Orin'
    
    user = WebhookBase(name = name)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())
    
    test_user = WebhookBase._create_empty(user_id)
    vampytest.assert_eq(test_user, test_user)
    vampytest.assert_ne(user, test_user)


def _iter_options__eq():
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
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'avatar': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'okuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'channel_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'webhook_type': WebhookType.bot,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__WebhookBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``WebhookBase.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    instance_0 = WebhookBase(**keyword_parameters_0)
    instance_1 = WebhookBase(**keyword_parameters_1)
    
    output = instance_0 == instance_1
    vampytest.assert_instance(output, bool)
    return output


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
