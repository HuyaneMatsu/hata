import vampytest

from ....bases import Icon, IconType
from ....emoji import Emoji
from ....sticker import Sticker

from ...guild import GuildFeature

from ..guild_preview import GuildPreview

from .test__GuildPreview__constructor import _assert_fields_set


def test__GuildPreview__from_data():
    """
    Tests whether ``GuildPreview.from_data`` works as intended.
    
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
    
    data = {
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
        'description': description,
        'discovery_splash': discovery_splash.as_base_16_hash,
        'emojis': [emoji.to_data(defaults = True, include_internals = True) for emoji in emojis],
        'features': [feature.value for feature in features],
        'id': str(guild_id),
        'icon': icon.as_base_16_hash,
        'splash': invite_splash.as_base_16_hash,
        'stickers': [sticker.to_data(defaults = True, include_internals = True) for sticker in stickers],
        'name': name,
    }
    
    guild_preview = GuildPreview.from_data(data)
    _assert_fields_set(guild_preview)
    
    vampytest.assert_eq(guild_preview.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild_preview.approximate_user_count, approximate_user_count)
    vampytest.assert_eq(guild_preview.description, description)
    vampytest.assert_eq(guild_preview.discovery_splash, discovery_splash)
    vampytest.assert_eq(guild_preview.emojis, {emoji.id: emoji for emoji in emojis})
    vampytest.assert_eq(guild_preview.features, tuple(features))
    vampytest.assert_eq(guild_preview.icon, icon)
    vampytest.assert_eq(guild_preview.id, guild_id)
    vampytest.assert_eq(guild_preview.invite_splash, invite_splash)
    vampytest.assert_eq(guild_preview.stickers, {sticker.id: sticker for sticker in stickers})
    vampytest.assert_eq(guild_preview.name, name)


def test__GuildFeature__to_data():
    """
    Tests whether ``GuildFeature.to_data`` works as intended.
    
    Case: Include defaults.
    """
    approximate_online_count = 13
    approximate_user_count = 14
    description = 'cordelia'
    discovery_splash = Icon(IconType.static, 12)
    emojis = [Emoji.precreate(202301080016, name = 'Koishi')]
    features = [GuildFeature.banner]
    guild_id = 202301080017
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 12)
    stickers = [Sticker.precreate(202301080018, name = 'Satori')]
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
    
    expected_output = {
        'approximate_presence_count': approximate_online_count,
        'approximate_member_count': approximate_user_count,
        'description': description,
        'discovery_splash': discovery_splash.as_base_16_hash,
        'emojis': [emoji.to_data(defaults = True, include_internals = True) for emoji in emojis],
        'features': [feature.value for feature in features],
        'id': str(guild_id),
        'icon': icon.as_base_16_hash,
        'splash': invite_splash.as_base_16_hash,
        'stickers': [sticker.to_data(defaults = True, include_internals = True) for sticker in stickers],
        'name': name,
    }
    
    vampytest.assert_eq(
        guild_preview.to_data(defaults = True),
        expected_output,
    )
