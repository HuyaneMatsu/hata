import vampytest

from ....bases import Icon, IconType
from ....emoji import Emoji
from ....sticker import Sticker

from ...guild import GuildFeature

from ..guild_preview import GuildPreview


def test__GuildPreview__repr():
    """
    Tests whether ``GuildPreview.__repr__`` works as intended.
    """
    approximate_online_count = 13
    approximate_user_count = 14
    description = 'cordelia'
    discovery_splash = Icon(IconType.static, 12)
    emojis = [Emoji.precreate(202301080019, name = 'Koishi')]
    features = [GuildFeature.banner]
    guild_id = 202301080020
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 12)
    stickers = [Sticker.precreate(202301080021, name = 'Satori')]
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
    
    vampytest.assert_instance(repr(guild_preview), str)


def test__GuildPreview__hash():
    """
    Tests whether ``GuildPreview.__hash__`` works as intended.
    """
    approximate_online_count = 13
    approximate_user_count = 14
    description = 'cordelia'
    discovery_splash = Icon(IconType.static, 12)
    emojis = [Emoji.precreate(202301080022, name = 'Koishi')]
    features = [GuildFeature.banner]
    guild_id = 202301080023
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 12)
    stickers = [Sticker.precreate(202301080024, name = 'Satori')]
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
    
    vampytest.assert_instance(hash(guild_preview), int)


def test__GuildPreview__eq():
    """
    Tests whether ``GuildPreview.__eq__`` works as intended.
    """
    approximate_online_count = 13
    approximate_user_count = 14
    description = 'cordelia'
    discovery_splash = Icon(IconType.static, 12)
    emojis = [Emoji.precreate(202301080025, name = 'Koishi')]
    features = [GuildFeature.banner]
    guild_id = 202301080026
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 12)
    stickers = [Sticker.precreate(202301080027, name = 'Satori')]
    name = 'Yurica'
    
    keyword_parameters = {
        'approximate_online_count': approximate_online_count,
        'approximate_user_count': approximate_user_count,
        'description': description,
        'discovery_splash': discovery_splash,
        'emojis': emojis,
        'features': features,
        'guild_id': guild_id,
        'icon': icon,
        'invite_splash': invite_splash,
        'stickers': stickers,
        'name': name,
    }
    
    guild_preview = GuildPreview(**keyword_parameters)
    
    vampytest.assert_eq(guild_preview, guild_preview)
    vampytest.assert_ne(guild_preview, object())
    
    for field_name, field_value in (
        ('approximate_online_count', 111),
        ('approximate_user_count', 112),
        ('description', None),
        ('discovery_splash', None),
        ('emojis', None),
        ('features', None),
        ('guild_id', 202301080028),
        ('icon', None),
        ('invite_splash', None),
        ('stickers', None),
        ('name', 'Flower'),
    ):
        test_guild_preview = GuildPreview(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(guild_preview, test_guild_preview)


def test__GuildPreview__format():
    """
    Tests whether ``GuildPreview.__format__`` works as intended.
    """
    guild_preview = GuildPreview()
    
    vampytest.assert_instance(format(guild_preview, ''), str)
    vampytest.assert_instance(format(guild_preview, 'c'), str)
