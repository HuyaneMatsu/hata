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


def test__Webhook__eq():
    """
    Tests whether ``Webhook.__eq__`` works as intended.
    """
    webhook_id = 202302050035
    
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050036
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
    
    webhook = Webhook(**keyword_parameters)
    vampytest.assert_eq(webhook, webhook)
    vampytest.assert_ne(webhook, object())

    test_webhook = Webhook._create_empty(webhook_id)
    vampytest.assert_eq(test_webhook, test_webhook)
    vampytest.assert_ne(webhook, test_webhook)
    
    for field_name, field_value in (
        ('avatar', None),
        ('name', 'okuu'),
        ('channel_id', 0),
        ('webhook_type', WebhookType.bot),
        ('application_id', 0),
        ('source_channel', None),
        ('source_guild', None),
        ('token', ''),
        ('user', ZEROUSER),
    ):
        test_webhook = Webhook(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(webhook, test_webhook)


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
