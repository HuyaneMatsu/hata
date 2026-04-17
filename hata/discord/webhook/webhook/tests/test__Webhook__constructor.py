import vampytest

from ....bases import Icon, IconType
from ....user import ClientUserBase, User

from ...webhook_source_channel import WebhookSourceChannel
from ...webhook_source_guild import WebhookSourceGuild

from ..preinstanced import WebhookType
from ..webhook import Webhook


def _assert_fields_set(webhook):
    """
    Asserts whether every fields of the given webhook are set.
    
    Parameters
    ----------
    webhook : ``Webhook``
        The webhook to check.
    """
    vampytest.assert_instance(webhook, Webhook)
    vampytest.assert_instance(webhook.avatar, Icon)
    vampytest.assert_instance(webhook.id, int)
    vampytest.assert_instance(webhook.name, str)
    vampytest.assert_instance(webhook.channel_id, int)
    vampytest.assert_instance(webhook.application_id, int)
    vampytest.assert_instance(webhook.source_channel, WebhookSourceChannel, nullable = True)
    vampytest.assert_instance(webhook.source_guild, WebhookSourceGuild, nullable = True)
    vampytest.assert_instance(webhook.token, str)
    vampytest.assert_instance(webhook.user, ClientUserBase)


def test__Webhook__new__0():
    """
    Tests whether ``Webhook.__new__`` works as intended.
    
    Case: No fields given.
    """
    webhook = Webhook()
    _assert_fields_set(webhook)


def test__Webhook__new__1():
    """
    Tests whether ``Webhook.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    name = 'voice in the dark'
    channel_id = 202302050028
    webhook_type = WebhookType.server
    application_id = 202302050045
    source_channel = WebhookSourceChannel(channel_id = 202302050046, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050047, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050048, name = 'seija')
    
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
    _assert_fields_set(webhook)
    
    vampytest.assert_eq(webhook.avatar, avatar)
    vampytest.assert_eq(webhook.name, name)
    vampytest.assert_eq(webhook.channel_id, channel_id)
    vampytest.assert_is(webhook.type, webhook_type)
    vampytest.assert_eq(webhook.application_id, application_id)
    vampytest.assert_eq(webhook.source_channel, source_channel)
    vampytest.assert_eq(webhook.source_guild, source_guild)
    vampytest.assert_eq(webhook.token, token)
    vampytest.assert_is(webhook.user, user)


def test__Webhook__create_empty():
    """
    Tests whether ``Webhook._create_empty`` works as intended.
    """
    webhook_id = 202302050029
    webhook = Webhook._create_empty(webhook_id)
    _assert_fields_set(webhook)
    
    vampytest.assert_eq(webhook.id, webhook_id)


def test__Webhook__precreate__0():
    """
    Tests whether ``Webhook.precreate`` works as intended.
    
    Case: No fields given.
    """
    webhook_id = 202302050049
    webhook = Webhook.precreate(webhook_id)
    
    _assert_fields_set(webhook)
    vampytest.assert_eq(webhook.id, webhook_id)


def test__Webhook__precreate__1():
    """
    Tests whether ``Webhook.precreate`` works as intended.
    
    Case: All fields given.
    """
    webhook_id = 202302050050
    
    avatar = Icon(IconType.static, 32)
    name = 'voice in the dark'
    channel_id = 202302050051
    webhook_type = WebhookType.server
    application_id = 202302050052
    source_channel = WebhookSourceChannel(channel_id = 202302050053, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050054, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050055, name = 'seija')
    
    webhook = Webhook.precreate(
        webhook_id,
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
    
    _assert_fields_set(webhook)
    vampytest.assert_eq(webhook.id, webhook_id)

    vampytest.assert_eq(webhook.avatar, avatar)
    vampytest.assert_eq(webhook.name, name)
    vampytest.assert_eq(webhook.channel_id, channel_id)
    vampytest.assert_is(webhook.type, webhook_type)
    vampytest.assert_eq(webhook.application_id, application_id)
    vampytest.assert_eq(webhook.source_channel, source_channel)
    vampytest.assert_eq(webhook.source_guild, source_guild)
    vampytest.assert_eq(webhook.token, token)
    vampytest.assert_is(webhook.user, user)


def test__Webhook__precreate__2():
    """
    Tests whether ``Webhook.precreate`` works as intended.
    
    Case: Caching
    """
    webhook_id = 202302050056
    webhook = Webhook.precreate(webhook_id)
    
    test_webhook = Webhook.precreate(webhook_id)
    vampytest.assert_is(webhook, test_webhook)



# Cannot test this yet, no client mocking available.
'''
def test__Webhook__from_follow_data():
    """
    Tests whether ``Webhook._from_follow_data`` works as intended.
    """
'''


def test__Webhook__from_url__0():
    """
    Tests whether ``Webhook.from_url`` works as intended.
    
    Case: Failing
    """
    url = 'derp'
    
    webhook = Webhook.from_url(url)
    vampytest.assert_is(webhook, None)



def test__Webhook__from_url__1():
    """
    Tests whether ``Webhook.from_url`` works as intended.
    
    Case: Passing.
    """
    # This actually needs to be a valid webhook or re-parsing fails
    webhook_id = 163175630562080216 # 202302050116
    token = 'nue' * 21
    
    webhook = Webhook(
        token = token,
    )
    webhook.id = webhook_id
    
    url = webhook.url
    
    webhook = Webhook.from_url(url)
    _assert_fields_set(webhook)
    vampytest.assert_eq(webhook.id, webhook_id)
    vampytest.assert_eq(webhook.token, token)
