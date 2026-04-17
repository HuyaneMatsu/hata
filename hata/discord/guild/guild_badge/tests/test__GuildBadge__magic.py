import vampytest

from ....bases import Icon, IconType

from ..guild_badge import GuildBadge


def test__GuildBadge__repr():
    """
    Tests whether ``GuildBadge.__repr__`` works as intended.
    """
    enabled = False
    guild_id = 202405170006
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    guild_badge = GuildBadge(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    vampytest.assert_instance(repr(guild_badge), str)


def test__GuildBadge__hash():
    """
    Tests whether ``GuildBadge.__hash__`` works as intended.
    """
    enabled = False
    guild_id = 202405170007
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    guild_badge = GuildBadge(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    vampytest.assert_instance(hash(guild_badge), int)


def test__GuildBadge__eq():
    """
    Tests whether ``GuildBadge.__eq__`` works as intended.
    """
    enabled = False
    guild_id = 202405170008
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    keyword_parameters = {
        'enabled': enabled,
        'guild_id': guild_id,
        'icon': icon,
        'tag': tag,
    }
    
    guild_badge = GuildBadge(**keyword_parameters)
    vampytest.assert_eq(guild_badge, guild_badge)
    vampytest.assert_ne(guild_badge, object())
    
    for field_tag, field_value in (
        ('enabled', True),
        ('guild_id', 202405170009),
        ('icon', Icon(IconType.animated, 14)),
        ('tag', 'OKUU'),
    ):
        test_guild = GuildBadge(**{**keyword_parameters, field_tag: field_value})
        vampytest.assert_ne(guild_badge, test_guild)
