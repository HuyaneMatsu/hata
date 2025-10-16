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


def test__WebhookBase__can_use_emoji__unicode():
    """
    Tests whether ``WebhookBase.can_use_emoji`` works as intended.
    
    Case: unicode.
    """
    channel_id = 202510010010
    
    emoji = BUILTIN_EMOJIS['heart']
    
    webhook = WebhookBase(channel_id = channel_id)
    
    output = webhook.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__WebhookBase__can_use_emoji__custom_allowed():
    """
    Tests whether ``WebhookBase.can_use_emoji`` works as intended.
    
    Case: custom & allowed.
    """
    emoji_id = 202510010030
    channel_id = 202510010031
    guild_id = 202510010032
    
    emoji = Emoji.precreate(
        emoji_id,
        name = 'satori',
        guild_id = guild_id,
    )
    
    channel = Channel.precreate(
        channel_id,
        guild_id = guild_id,
    )
    
    role = Role.precreate(
        guild_id,
        permissions = Permission().update_by_keys(use_external_emojis = True),
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel],
        roles = [role],
    )
    
    webhook = WebhookBase(channel_id = channel_id)
    
    output = webhook.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__WebhookBase__can_use_emoji__custom_not_available():
    """
    Tests whether ``WebhookBase.can_use_emoji`` works as intended.
    
    Case: custom & not available.
    """
    emoji_id = 202510010040
    channel_id = 202510010041
    guild_id = 202510010042
    
    emoji = Emoji.precreate(
        emoji_id,
        name = 'satori',
        guild_id = guild_id,
        available = False,
    )
    
    channel = Channel.precreate(
        channel_id,
        guild_id = guild_id,
    )
    
    role = Role.precreate(
        guild_id,
        permissions = Permission().update_by_keys(use_external_emojis = True),
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel],
        roles = [role],
    )
    
    webhook = WebhookBase(channel_id = channel_id)
    
    output = webhook.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__WebhookBase__can_use_emoji__custom_role_bound():
    """
    Tests whether ``WebhookBase.can_use_emoji`` works as intended.
    
    Case: custom & role bound.
    """
    emoji_id = 202510010050
    channel_id = 202510010051
    guild_id = 202510010052
    
    role_id_bound = 202510010053
    
    emoji = Emoji.precreate(
        emoji_id,
        name = 'satori',
        guild_id = guild_id,
        role_ids = [role_id_bound],
    )
    
    channel = Channel.precreate(
        channel_id,
        guild_id = guild_id,
    )
    
    role = Role.precreate(
        guild_id,
        permissions = Permission().update_by_keys(use_external_emojis = True),
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel],
        roles = [role],
    )
    
    webhook = WebhookBase(channel_id = channel_id)
    
    output = webhook.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__WebhookBase__can_use_emoji__custom_guild_not_cached():
    """
    Tests whether ``WebhookBase.can_use_emoji`` works as intended.
    
    Case: custom & guild not cached.
    """
    emoji_id = 202510010060
    channel_id = 202510010061
    guild_id = 202510010062
    
    emoji = Emoji.precreate(
        emoji_id,
        name = 'satori',
        guild_id = guild_id,
    )
    
    channel = Channel.precreate(
        channel_id,
        guild_id = guild_id,
    )
    
    role = Role.precreate(
        guild_id,
        permissions = Permission().update_by_keys(use_external_emojis = True),
    )
    
    webhook = WebhookBase(channel_id = channel_id)
    
    output = webhook.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__WebhookBase__can_use_emoji__custom_no_guild_default_role():
    """
    Tests whether ``WebhookBase.can_use_emoji`` works as intended.
    
    Case: custom & guild has no default role.
    """
    emoji_id = 202510010070
    channel_id = 202510010071
    guild_id = 202510010072
    
    emoji = Emoji.precreate(
        emoji_id,
        name = 'satori',
        guild_id = guild_id,
    )
    
    channel = Channel.precreate(
        channel_id,
        guild_id = guild_id,
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel],
        roles = [],
    )
    
    webhook = WebhookBase(channel_id = channel_id)
    
    output = webhook.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__WebhookBase__can_use_emoji__custom_no_permissions():
    """
    Tests whether ``WebhookBase.can_use_emoji`` works as intended.
    
    Case: custom & allowed.
    """
    emoji_id = 202510010080
    channel_id = 202510010081
    guild_id = 202510010082
    
    emoji = Emoji.precreate(
        emoji_id,
        name = 'satori',
        guild_id = guild_id,
    )
    
    channel = Channel.precreate(
        channel_id,
        guild_id = guild_id,
    )
    
    role = Role.precreate(
        guild_id,
        permissions = Permission(),
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel],
        roles = [role],
    )
    
    webhook = WebhookBase(channel_id = channel_id)
    
    output = webhook.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
