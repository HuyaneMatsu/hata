import vampytest

from ....bases import Icon, IconType

from ..user_clan import UserClan


def test__UserClan__repr():
    """
    Tests whether ``UserClan.__repr__`` works as intended.
    """
    enabled = False
    guild_id = 202405170006
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    user_clan = UserClan(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    vampytest.assert_instance(repr(user_clan), str)


def test__UserClan__hash():
    """
    Tests whether ``UserClan.__hash__`` works as intended.
    """
    enabled = False
    guild_id = 202405170007
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    user_clan = UserClan(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    vampytest.assert_instance(hash(user_clan), int)


def test__UserClan__eq():
    """
    Tests whether ``UserClan.__eq__`` works as intended.
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
    
    user_clan = UserClan(**keyword_parameters)
    vampytest.assert_eq(user_clan, user_clan)
    vampytest.assert_ne(user_clan, object())
    
    for field_tag, field_value in (
        ('enabled', True),
        ('guild_id', 202405170009),
        ('icon', Icon(IconType.animated, 14)),
        ('tag', 'OKUU'),
    ):
        test_guild = UserClan(**{**keyword_parameters, field_tag: field_value})
        vampytest.assert_ne(user_clan, test_guild)
