import vampytest

from ....bases import IconType, Icon
from ....user import User

from ...webhook_source_channel import WebhookSourceChannel
from ...webhook_source_guild import WebhookSourceGuild

from ..preinstanced import WebhookType
from ..webhook import Webhook

from .test__Webhook__constructor import _assert_fields_set

    
def test__Webhook__from_data__0():
    """
    Tests whether ``Webhook.from_data`` works as intended.
    
    Case: Creation.
    """
    webhook_id = 202302050062
    avatar = Icon(IconType.static, 32)
    name = 'voice in the dark'
    channel_id = 202302050057
    webhook_type = WebhookType.server
    application_id = 202302050058
    source_channel = WebhookSourceChannel(channel_id = 202302050059, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050060, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050061, name = 'seija')

    data = {
        'avatar': avatar.as_base_16_hash,
        'name': name,
        'id': str(webhook_id),
        'channel_id': str(channel_id),
        'type': webhook_type.value,
        'application_id': str(application_id),
        'source_channel': source_channel.to_data(defaults = True),
        'source_guild': source_guild.to_data(defaults = True),
        'token': token,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    webhook = Webhook.from_data(data)
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
    
        
def test__Webhook__from_data__1():
    """
    Tests whether ``Webhook.from_data`` works as intended.
    
    Case: Caching.
    """
    webhook_id = 202302050063
    
    data = {
        'id': str(webhook_id),
    }
    
    webhook = Webhook.from_data(data)
    test_webhook = Webhook.from_data(data)
    
    vampytest.assert_is(webhook, test_webhook)


def test__Webhook__to_data():
    """
    Tests whether ``Webhook.to_data`` works as intended.
    
    Case: Include internals and defaults.
    """
    webhook_id = 202302050030
    name = 'suika'
    avatar = Icon(IconType.static, 24)
    channel_id = 202302050064
    webhook_type = WebhookType.server
    application_id = 202302050065
    source_channel = WebhookSourceChannel(channel_id = 202302050066, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050067, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050068, name = 'seija')
    
    webhook = Webhook(
        name = name,
        avatar = avatar,
        channel_id = channel_id,
        webhook_type = webhook_type,
        application_id = application_id,
        source_channel = source_channel,
        source_guild = source_guild,
        token = token,
        user = user,
    )
    webhook.id = webhook_id
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': None,
        'accent_color': None,
        'discriminator': '0000',
        'global_name': None,
        'username': name,
        'banner': None,
        'id': str(webhook_id),
        'public_flags': 0,
        'bot': True,
    }
    
    vampytest.assert_eq(
        webhook.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Webhook__to_webhook_data():
    """
    Tests whether ``Webhook.to_webhook_data`` works as intended.
    
    Case: Include internals and defaults.
    """
    webhook_id = 202302050069
    name = 'suika'
    avatar = Icon(IconType.static, 24)
    channel_id = 202302050070
    webhook_type = WebhookType.server
    application_id = 202302050071
    source_channel = WebhookSourceChannel(channel_id = 202302050072, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050073, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050074, name = 'seija')
    
    webhook = Webhook(
        name = name,
        avatar = avatar,
        channel_id = channel_id,
        webhook_type = webhook_type,
        application_id = application_id,
        source_channel = source_channel,
        source_guild = source_guild,
        token = token,
        user = user,
    )
    webhook.id = webhook_id
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'name': name,
        'id': str(webhook_id),
        'channel_id': str(channel_id),
        'type': webhook_type.value,
        'application_id': str(application_id),
        'source_channel': source_channel.to_data(defaults = True),
        'source_guild': source_guild.to_data(defaults = True),
        'token': token,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    vampytest.assert_eq(
        webhook.to_webhook_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Webhook__update_attributes():
    """
    Tests whether ``Webhook._update_attributes` works as intended.
    """
    name = 'suika'
    avatar = Icon(IconType.static, 24)
    channel_id = 202302050075
    
    webhook = Webhook()
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'name': name,
        'channel_id': str(channel_id),
    }
    
    webhook._update_attributes(data)
    
    vampytest.assert_eq(webhook.name, name)
    vampytest.assert_eq(webhook.avatar, avatar)
    vampytest.assert_eq(webhook.channel_id, channel_id)


def test__Webhook__difference_update_attributes():
    """
    Tests whether ``Webhook._difference_update_attributes` works as intended.
    """
    old_name = 'suika'
    old_avatar = Icon(IconType.static, 24)
    old_channel_id = 202302050076
    new_name = 'ibuki'
    new_avatar = Icon(IconType.animated, 13)
    new_channel_id = 202302050077
    
    webhook = Webhook(
        avatar = old_avatar,
        name = old_name,
        channel_id = old_channel_id,
    )
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'name': new_name,
        'channel_id': str(new_channel_id),
    }
    
    old_attributes = webhook._difference_update_attributes(data)
    
    vampytest.assert_eq(webhook.name, new_name)
    vampytest.assert_eq(webhook.avatar, new_avatar)
    vampytest.assert_eq(webhook.channel_id, new_channel_id)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'name': old_name,
            'avatar': old_avatar,
            'channel_id': old_channel_id,
        },
    )


def test__Webhook__set_attributes():
    """
    Tests whether ``Webhook._set_attributes`` works as intended.
    
    Case: Creation.
    """
    avatar = Icon(IconType.static, 32)
    name = 'voice in the dark'
    channel_id = 202302050078
    webhook_type = WebhookType.server
    application_id = 202302050079
    source_channel = WebhookSourceChannel(channel_id = 202302050080, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050081, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050082, name = 'seija')

    data = {
        'avatar': avatar.as_base_16_hash,
        'name': name,
        'channel_id': str(channel_id),
        'type': webhook_type.value,
        'application_id': str(application_id),
        'source_channel': source_channel.to_data(defaults = True),
        'source_guild': source_guild.to_data(defaults = True),
        'token': token,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    webhook = Webhook()
    webhook._set_attributes(data)
    
    vampytest.assert_eq(webhook.avatar, avatar)
    vampytest.assert_eq(webhook.name, name)
    vampytest.assert_eq(webhook.channel_id, channel_id)
    vampytest.assert_is(webhook.type, webhook_type)
    vampytest.assert_eq(webhook.application_id, application_id)
    vampytest.assert_eq(webhook.source_channel, source_channel)
    vampytest.assert_eq(webhook.source_guild, source_guild)
    vampytest.assert_eq(webhook.token, token)
    vampytest.assert_is(webhook.user, user)
