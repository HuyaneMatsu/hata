import vampytest

from ....bases import Icon, IconType

from ..user_clan import UserClan


def _assert_fields_set(user_clan):
    """
    Asserts whether every fields are set of the given user clan.
    
    Parameters
    ----------
    user_clan : ``UserClan``
        The user clan to check.
    """
    vampytest.assert_instance(user_clan, UserClan)
    vampytest.assert_instance(user_clan.enabled, bool)
    vampytest.assert_instance(user_clan.guild_id, int)
    vampytest.assert_instance(user_clan.icon, Icon)
    vampytest.assert_instance(user_clan.tag, str)


def test__UserClan__new__no_fields():
    """
    Tests whether ``UserClan.__new__`` works as intended.
    
    Case: No fields given.
    """
    user_clan = UserClan()
    _assert_fields_set(user_clan)


def test__UserClan__new__all_fields():
    """
    Tests whether ``UserClan.__new__`` works as intended.
    
    Case: All fields given.
    """
    enabled = False
    guild_id = 202405170003
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    user_clan = UserClan(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    _assert_fields_set(user_clan)
    
    vampytest.assert_eq(user_clan.enabled, enabled)
    vampytest.assert_eq(user_clan.guild_id, guild_id)
    vampytest.assert_eq(user_clan.icon, icon)
    vampytest.assert_eq(user_clan.tag, tag)
