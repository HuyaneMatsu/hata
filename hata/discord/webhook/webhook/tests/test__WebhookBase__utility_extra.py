import vampytest

from ....channel import Channel
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji
from ....guild import Guild
from ....permission import Permission
from ....role import Role
from ....user import ClientUserBase

from ...webhook_source_channel import WebhookSourceChannel
from ...webhook_source_guild import WebhookSourceGuild

from ..webhook_base import WebhookBase


def test__WebhookBase__bot():
    """
    Tests whether ``WebhookBase.bot`` works as intended.
    """
    webhook = WebhookBase()
    output = webhook.bot
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__WebhookBase__placeholders():
    """
    Tests whether ``WebhookBase``'s placeholders work as intended.
    """
    webhook = WebhookBase()
    vampytest.assert_instance(webhook.application_id, int)
    vampytest.assert_instance(webhook.source_channel, WebhookSourceChannel, nullable = True)
    vampytest.assert_instance(webhook.source_guild, WebhookSourceGuild, nullable = True)
    vampytest.assert_instance(webhook.token, str)
    vampytest.assert_instance(webhook.user, ClientUserBase)


def test__WebhookBase__partial():
    """
    Tests whether ``WebhookBase.partial`` works as intended.
    """
    channel_id = 202302050016
    guild_id = 202302050017
    
    webhook = WebhookBase()
    vampytest.assert_true(webhook.partial)
    
    webhook = WebhookBase(channel_id = channel_id)
    vampytest.assert_true(webhook.partial)
    
    channel = Channel.precreate(channel_id, guild_id = guild_id)
    vampytest.assert_true(webhook.partial)
    
    guild = Guild.precreate(guild_id)
    vampytest.assert_false(webhook.partial)


def test__WebhookBase__guild():
    """
    Tests whether ``WebhookBase.guild`` works as intended.
    """
    channel_id = 202302050018
    guild_id = 202302050019
    
    webhook = WebhookBase(channel_id = channel_id)
    channel = Channel.precreate(channel_id, guild_id = guild_id)
    guild = Guild.precreate(guild_id)
    
    vampytest.assert_is(webhook.guild, guild)


def test__WebhookBase__can_use_emoji():
    """
    Tests whether ``WebhookBase.can_use_emoji`` works as intended.
    """
    channel_id = 202302050020
    guild_id = 202302050021
    
    webhook = WebhookBase(channel_id = channel_id)
    channel = Channel.precreate(channel_id, guild_id = guild_id)
    guild = Guild.precreate(guild_id)
    
    emoji = BUILTIN_EMOJIS['x']
    vampytest.assert_true(webhook.can_use_emoji(emoji))
    
    emoji = Emoji.precreate(202302050022, role_ids = [202302050023])
    vampytest.assert_false(webhook.can_use_emoji(emoji))
    
    role = Role.precreate(guild_id)
    guild.roles[guild_id] = role
    
    
    vampytest.assert_false(webhook.can_use_emoji(emoji))
    
    role.permissions = Permission().update_by_keys(use_external_emojis = True)
    vampytest.assert_false(webhook.can_use_emoji(emoji))
