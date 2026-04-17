import vampytest

from ....bases import Icon, IconType
from ....user import User, ZEROUSER

from ...webhook_source_channel import WebhookSourceChannel
from ...webhook_source_guild import WebhookSourceGuild

from ..preinstanced import WebhookType
from ..webhook import Webhook


def test__Webhook__repr():
    """
    Tests whether ``Webhook.__repr__`` works as intended.
    """
    webhook_id = 202302050031
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050032
    webhook_type = WebhookType.server
    application_id = 202302050083
    source_channel = WebhookSourceChannel(channel_id = 202302050084, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050085, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050086, name = 'seija')
    
    webhook = Webhook._create_empty(webhook_id)
    vampytest.assert_instance(repr(webhook), str)

    webhook = Webhook(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
        application_id = application_id,
        source_channel = source_channel,
        source_guild = source_guild,
        token = token,
        user = user,
    )
    vampytest.assert_instance(repr(webhook), str)


def test__Webhook__hash():
    """
    Tests whether ``Webhook.__hash__`` works as intended.
    """
    webhook_id = 202302050033
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050034
    webhook_type = WebhookType.server
    application_id = 202302050087
    source_channel = WebhookSourceChannel(channel_id = 202302050088, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050089, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050090, name = 'seija')
    
    webhook = Webhook._create_empty(webhook_id)
    vampytest.assert_instance(repr(webhook), str)

    webhook = Webhook(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
        application_id = application_id,
        source_channel = source_channel,
        source_guild = source_guild,
        token = token,
        user = user,
    )
    vampytest.assert_instance(repr(webhook), str)


def test__Webhook__eq__non_partial_and_different_object():
    """
    Tests whether ``Webhook.__eq__`` works as intended.
    
    Case: non partial and non user object.
    """
    user_id = 202504260016
    
    name = 'Orin'
    
    user = Webhook(name = name)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())
    
    test_user = Webhook._create_empty(user_id)
    vampytest.assert_eq(test_user, test_user)
    vampytest.assert_ne(user, test_user)


def _iter_options__eq():
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050007
    webhook_type = WebhookType.server
    application_id = 202302050091
    source_channel = WebhookSourceChannel(channel_id = 202302050092, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050093, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050094, name = 'seija')
    
    keyword_parameters = {
        'avatar': avatar,
        'name': name,
        'channel_id': channel_id,
        'webhook_type': webhook_type,
        'application_id': application_id,
        'source_channel': source_channel,
        'source_guild': source_guild,
        'token': token,
        'user': user,
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
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'source_channel': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'source_guild': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'token': '',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user': ZEROUSER,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Webhook__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Webhook.__eq__`` works as intended.
    
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
    instance_0 = Webhook(**keyword_parameters_0)
    instance_1 = Webhook(**keyword_parameters_1)
    
    output = instance_0 == instance_1
    vampytest.assert_instance(output, bool)
    return output


def test__Webhook__format():
    """
    Tests whether ``Webhook.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050037
    webhook_type = WebhookType.server
    application_id = 202302050095
    source_channel = WebhookSourceChannel(channel_id = 202302050096, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050097, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050098, name = 'seija')
    
    webhook = Webhook(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        webhook_type = webhook_type,
        application_id = application_id,
        source_channel = source_channel,
        source_guild = source_guild,
        token = token,
        user = user,
    )
    
    vampytest.assert_instance(format(webhook, ''), str)


def test__Webhook__sort():
    """
    Tests whether sorting ``Webhook` works as intended.
    """
    webhook_id_0 = 202302050038
    webhook_id_1 = 202302050039
    webhook_id_2 = 202302050040
    
    webhook_0 = Webhook._create_empty(webhook_id_0)
    webhook_1 = Webhook._create_empty(webhook_id_1)
    webhook_2 = Webhook._create_empty(webhook_id_2)
    
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
