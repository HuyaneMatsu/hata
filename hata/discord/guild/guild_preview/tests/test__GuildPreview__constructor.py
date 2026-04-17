import vampytest

from ....bases import Icon, IconType
from ....emoji import Emoji
from ....sticker import Sticker

from ...guild import GuildFeature

from ..guild_preview import GuildPreview


def _assert_fields_set(guild_preview):
    """
    Asserts whether every fields are set of the guild guild preview.
    
    Parameters
    ----------
    guild_preview : ``GuildPreview`
        The guild preview to check.
    """
    vampytest.assert_instance(guild_preview, GuildPreview)
    vampytest.assert_instance(guild_preview.approximate_online_count, int)
    vampytest.assert_instance(guild_preview.approximate_user_count, int)
    vampytest.assert_instance(guild_preview.description, str, nullable = True)
    vampytest.assert_instance(guild_preview.discovery_splash, Icon)
    vampytest.assert_instance(guild_preview.emojis, dict)
    vampytest.assert_instance(guild_preview.features, tuple, nullable = True)
    vampytest.assert_instance(guild_preview.icon, Icon)
    vampytest.assert_instance(guild_preview.id, int)
    vampytest.assert_instance(guild_preview.invite_splash, Icon, nullable = True)
    vampytest.assert_instance(guild_preview.stickers, dict)
    vampytest.assert_instance(guild_preview.name, str)


def test__GuildPreview__new__0():
    """
    Tests whether ``GuildPreview.__new__`` works as intended.
    
    Case: No fields given.
    """
    guild_preview = GuildPreview()
    _assert_fields_set(guild_preview)


def test__GuildPreview__new__1():
    """
    Tests whether ``GuildPreview.__new__`` works as intended.
    
    Case: All fields given.
    """
    approximate_online_count = 13
    approximate_user_count = 14
    description = 'cordelia'
    discovery_splash = Icon(IconType.static, 12)
    emojis = [Emoji.precreate(202301080013, name = 'Koishi')]
    features = [GuildFeature.banner]
    guild_id = 202301080014
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 12)
    stickers = [Sticker.precreate(202301080015, name = 'Satori')]
    name = 'Yurica'
    
    guild_preview = GuildPreview(
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
        description = description,
        discovery_splash = discovery_splash,
        emojis = emojis,
        features = features,
        guild_id = guild_id,
        icon = icon,
        invite_splash = invite_splash,
        stickers = stickers,
        name = name,
    )
    _assert_fields_set(guild_preview)
    
    vampytest.assert_eq(guild_preview.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild_preview.approximate_user_count, approximate_user_count)
    vampytest.assert_eq(guild_preview.description, description)
    vampytest.assert_eq(guild_preview.discovery_splash, discovery_splash)
    vampytest.assert_eq(guild_preview.emojis, {emoji.id: emoji for emoji in emojis})
    vampytest.assert_eq(guild_preview.features, tuple(features))
    vampytest.assert_eq(guild_preview.id, guild_id)
    vampytest.assert_eq(guild_preview.icon, icon)
    vampytest.assert_eq(guild_preview.invite_splash, invite_splash)
    vampytest.assert_eq(guild_preview.stickers, {sticker.id: sticker for sticker in stickers})
    vampytest.assert_eq(guild_preview.name, name)
