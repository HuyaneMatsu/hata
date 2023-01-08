import vampytest

from ....bases import Icon, IconType
from ....emoji import Emoji
from ....sticker import Sticker

from ...guild import GuildFeature

from ..guild_preview import GuildPreview

from .test__GuildPreview__constructor import _assert_fields_set


def test__GuildPreview__copy():
    """
    Tests whether ``GuildPreview.copy`` works as intended.
    """
    approximate_online_count = 13
    approximate_user_count = 14
    description = 'cordelia'
    discovery_splash = Icon(IconType.static, 12)
    emojis = [Emoji.precreate(202301080029, name = 'Koishi')]
    features = [GuildFeature.banner]
    guild_id = 202301080030
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 12)
    stickers = [Sticker.precreate(202301080031, name = 'Satori')]
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
    
    copy = guild_preview.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_preview)
    
    vampytest.assert_eq(copy, guild_preview)


def test__GuildPreview__copy_with__0():
    """
    Tests whether ``GuildPreview.copy_with`` works as intended.
    
    Case: No fields given.
    """
    approximate_online_count = 13
    approximate_user_count = 14
    description = 'cordelia'
    discovery_splash = Icon(IconType.static, 12)
    emojis = [Emoji.precreate(202301080032, name = 'Koishi')]
    features = [GuildFeature.banner]
    guild_id = 202301080033
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 12)
    stickers = [Sticker.precreate(202301080034, name = 'Satori')]
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
    
    copy = guild_preview.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_preview)
    
    vampytest.assert_eq(copy, guild_preview)


def test__GuildPreview__copy_with__1():
    """
    Tests whether ``GuildPreview.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_approximate_online_count = 13
    old_approximate_user_count = 14
    old_description = 'cordelia'
    old_discovery_splash = Icon(IconType.static, 12)
    old_emojis = [Emoji.precreate(202301080035, name = 'Koishi')]
    old_features = [GuildFeature.banner]
    old_guild_id = 202301080036
    old_icon = Icon(IconType.static, 11)
    old_invite_splash = Icon(IconType.animated, 12)
    old_stickers = [Sticker.precreate(202301080037, name = 'Satori')]
    old_name = 'Yurica'
    new_approximate_online_count = 111
    new_approximate_user_count = 112
    new_description = 'Yakumo'
    new_discovery_splash = Icon(IconType.animated, 3)
    new_emojis = [Emoji.precreate(202301080038, name = 'Orin')]
    new_features = [GuildFeature.animated_icon]
    new_guild_id = 202301080039
    new_icon = Icon(IconType.static, IconType.animated)
    new_invite_splash = Icon(IconType.static, 4)
    new_stickers = [Sticker.precreate(202301080040, name = 'Okuu')]
    new_name = 'Yukari'
    
    guild_preview = GuildPreview(
        approximate_online_count = old_approximate_online_count,
        approximate_user_count = old_approximate_user_count,
        description = old_description,
        discovery_splash = old_discovery_splash,
        emojis = old_emojis,
        features = old_features,
        guild_id = old_guild_id,
        icon = old_icon,
        invite_splash = old_invite_splash,
        stickers = old_stickers,
        name = old_name,
    )
    
    copy = guild_preview.copy_with(
        approximate_online_count = new_approximate_online_count,
        approximate_user_count = new_approximate_user_count,
        description = new_description,
        discovery_splash = new_discovery_splash,
        emojis = new_emojis,
        features = new_features,
        guild_id = new_guild_id,
        icon = new_icon,
        invite_splash = new_invite_splash,
        stickers = new_stickers,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_preview)
    
    
    vampytest.assert_eq(copy.approximate_online_count, new_approximate_online_count)
    vampytest.assert_eq(copy.approximate_user_count, new_approximate_user_count)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.discovery_splash, new_discovery_splash)
    vampytest.assert_eq(copy.emojis, {emoji.id: emoji for emoji in new_emojis})
    vampytest.assert_eq(copy.features, tuple(new_features))
    vampytest.assert_eq(copy.id, new_guild_id)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.invite_splash, new_invite_splash)
    vampytest.assert_eq(copy.stickers, {sticker.id: sticker for sticker in new_stickers})
    vampytest.assert_eq(copy.name, new_name)


def test__GuildPreview__iter_features():
    """
    Tests whether ``GuildPreview.iter_features`` works as intended.
    """
    for guild_preview, expected_output in (
        (
            GuildPreview(features = []),
            [],
        ), (
            GuildPreview(features = [GuildFeature.animated_banner, GuildFeature.animated_icon]),
            [GuildFeature.animated_banner, GuildFeature.animated_icon],
        ),
    ):
        vampytest.assert_eq([*guild_preview.iter_features()], expected_output)


def test__GuildPreview__has_feature():
    """
    Tests whether ``GuildPreview.has_feature`` works as intended.
    """
    feature = GuildFeature.animated_icon
    for guild_preview, expected_output in (
        (GuildPreview(features = []), False),
        (GuildPreview(features = [GuildFeature.animated_banner]), False),
        (GuildPreview(features = [feature]), True),
        (GuildPreview(features = [GuildFeature.animated_banner, feature]), True),
    ):
        vampytest.assert_eq(guild_preview.has_feature(feature), expected_output)
