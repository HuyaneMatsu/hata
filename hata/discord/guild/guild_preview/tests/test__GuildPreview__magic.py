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
    home_splash = Icon(IconType.static, 12)
    guild_id = 202301080020
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 14)
    stickers = [Sticker.precreate(202301080021, name = 'Satori')]
    name = 'Yurica'
    
    guild_preview = GuildPreview(
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
        description = description,
        discovery_splash = discovery_splash,
        emojis = emojis,
        features = features,
        home_splash = home_splash,
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
    home_splash = Icon(IconType.static, 12)
    guild_id = 202301080023
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 14)
    stickers = [Sticker.precreate(202301080024, name = 'Satori')]
    name = 'Yurica'
    
    guild_preview = GuildPreview(
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
        description = description,
        discovery_splash = discovery_splash,
        emojis = emojis,
        features = features,
        home_splash = home_splash,
        guild_id = guild_id,
        icon = icon,
        invite_splash = invite_splash,
        stickers = stickers,
        name = name,
    )
    
    vampytest.assert_instance(hash(guild_preview), int)


def _iter_options__eq():
    approximate_online_count = 13
    approximate_user_count = 14
    description = 'cordelia'
    discovery_splash = Icon(IconType.static, 12)
    emojis = [Emoji.precreate(202301080025, name = 'Koishi')]
    features = [GuildFeature.banner]
    home_splash = Icon(IconType.static, 12)
    guild_id = 202301080026
    icon = Icon(IconType.static, 11)
    invite_splash = Icon(IconType.animated, 14)
    stickers = [Sticker.precreate(202301080027, name = 'Satori')]
    name = 'Yurica'
    
    keyword_parameters = {
        'approximate_online_count': approximate_online_count,
        'approximate_user_count': approximate_user_count,
        'description': description,
        'discovery_splash': discovery_splash,
        'emojis': emojis,
        'features': features,
        'home_splash': home_splash,
        'guild_id': guild_id,
        'icon': icon,
        'invite_splash': invite_splash,
        'stickers': stickers,
        'name': name,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'approximate_online_count': 111,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'approximate_user_count': 112,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'discovery_splash': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'emojis': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'features': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'home_splash': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 202301080028,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'icon': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'invite_splash': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'stickers': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Flower',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__GuildPreview__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``GuildPreview.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    guild_preview_0 = GuildPreview(**keyword_parameters_0)
    guild_preview_1 = GuildPreview(**keyword_parameters_1)
    
    output = guild_preview_0 == guild_preview_1
    vampytest.assert_instance(output, bool)
    return output


def test__GuildPreview__format():
    """
    Tests whether ``GuildPreview.__format__`` works as intended.
    """
    guild_preview = GuildPreview()
    
    vampytest.assert_instance(format(guild_preview, ''), str)
    vampytest.assert_instance(format(guild_preview, 'c'), str)
