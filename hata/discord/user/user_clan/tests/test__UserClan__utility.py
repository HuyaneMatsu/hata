import vampytest

from ....bases import Icon, IconType
from ....guild import Guild

from ..user_clan import UserClan

from .test__UserClan__constructor import _assert_fields_set


def test__UserClan__copy():
    """
    Tests whether ``UserClan.copy`` works as intended.
    """
    enabled = False
    guild_id = 202405170010
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    guild = UserClan(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    copy = guild.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild)
    
    vampytest.assert_eq(copy, guild)


def test__UserClan__copy_with__no_fields():
    """
    Tests whether ``UserClan.copy_with`` works as intended.
    
    Case: No fields given.
    """
    enabled = False
    guild_id = 202405170011
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    guild = UserClan(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    copy = guild.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild)
    
    vampytest.assert_eq(copy, guild)


def test__UserClan__copy_with__all_fields():
    """
    Tests whether ``UserClan.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_enabled = False
    old_guild_id = 202405170012
    old_icon = Icon(IconType.static, 12)
    old_tag = 'ORIN'
    
    new_enabled = True
    new_guild_id = 202405170013
    new_icon = Icon(IconType.animated, 13)
    new_tag = 'OKUU'
    
    user_clan = UserClan(
        enabled = old_enabled,
        guild_id = old_guild_id,
        icon = old_icon,
        tag = old_tag,
    )
    copy = user_clan.copy_with(
        enabled = new_enabled,
        guild_id = new_guild_id,
        icon = new_icon,
        tag = new_tag,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, user_clan)

    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.tag, new_tag)


def _iter_options__guild():
    guild_id_0 = 202405170014
    guild_id_1 = 202405170015
    
    yield 0, None
    yield guild_id_0, None
    yield guild_id_1, Guild.precreate(guild_id_1)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__UserClan__guild(guild_id):
    """
    Tests whether ``UserClan.guild`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to test with.
    
    Returns
    -------
    guild : `None | Guild`
    """
    user_clan = UserClan(
        guild_id = guild_id,
    )
    
    output = user_clan.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output
