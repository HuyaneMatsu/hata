import vampytest

from ....bases import Icon, IconType
from ....user import User

from ...webhook_source_channel import WebhookSourceChannel
from ...webhook_source_guild import WebhookSourceGuild

from ..preinstanced import WebhookType
from ..webhook import Webhook

from .test__Webhook__constructor import _assert_fields_set


def test__Webhook__copy():
    """
    Tests whether ``Webhook.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050041
    webhook_type = WebhookType.server
    application_id = 202302050099
    source_channel = WebhookSourceChannel(channel_id = 202302050100, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050101, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050102, name = 'seija')
    
    webhook = Webhook(
        avatar = avatar,
        name = name,
        channel_id = channel_id,
        application_id = application_id,
        source_channel = source_channel,
        source_guild = source_guild,
        token = token,
        user = user,
        webhook_type = webhook_type,
    )
    
    copy = webhook.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(webhook, copy)
    
    vampytest.assert_eq(webhook, copy)


def test__Webhook__copy_with__0():
    """
    Tests whether ``Webhook.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    channel_id = 202302050042
    webhook_type = WebhookType.server
    application_id = 202302050103
    source_channel = WebhookSourceChannel(channel_id = 202302050104, name = 'keine')
    source_guild = WebhookSourceGuild(guild_id = 202302050105, name = 'mokou')
    token = 'nue'
    user = User.precreate(202302050106, name = 'seija')
    
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
    
    copy = webhook.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(webhook, copy)
    
    vampytest.assert_eq(webhook, copy)


def test__Webhook__copy_with__1():
    """
    Tests whether ``Webhook.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 14)
    old_name = 'orin'
    old_channel_id = 202302050043
    old_webhook_type = WebhookType.server
    old_application_id = 202302050107
    old_source_channel = WebhookSourceChannel(channel_id = 202302050108, name = 'keine')
    old_source_guild = WebhookSourceGuild(guild_id = 202302050109, name = 'mokou')
    old_token = 'nue'
    old_user = User.precreate(202302050110, name = 'seija')
    
    new_avatar = Icon(IconType.animated, 23)
    new_name = 'okuu'
    new_channel_id = 202302050044
    new_webhook_type = WebhookType.server
    new_application_id = 202302050112
    new_source_channel = WebhookSourceChannel(channel_id = 202302050111, name = 'keine')
    new_source_guild = WebhookSourceGuild(guild_id = 202302050113, name = 'mokou')
    new_token = 'nue'
    new_user = User.precreate(202302050114, name = 'seija')
    
    webhook = Webhook(
        avatar = old_avatar,
        name = old_name,
        channel_id = old_channel_id,
        webhook_type = old_webhook_type,
        application_id = old_application_id,
        source_channel = old_source_channel,
        source_guild = old_source_guild,
        token = old_token,
        user = old_user,
    )
    
    copy = webhook.copy_with(
        avatar = new_avatar,
        name = new_name,
        channel_id = new_channel_id,
        webhook_type = new_webhook_type,
        application_id = new_application_id,
        source_channel = new_source_channel,
        source_guild = new_source_guild,
        token = new_token,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(webhook, copy)
    
    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_is(copy.type, new_webhook_type)
    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.source_channel, new_source_channel)
    vampytest.assert_eq(copy.source_guild, new_source_guild)
    vampytest.assert_eq(copy.token, new_token)
    vampytest.assert_is(copy.user, new_user)
