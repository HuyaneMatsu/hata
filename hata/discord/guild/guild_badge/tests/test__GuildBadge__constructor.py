import vampytest

from ....bases import Icon, IconType

from ..guild_badge import GuildBadge


def _assert_fields_set(guild_badge):
    """
    Asserts whether every fields are set of the given guild badge.
    
    Parameters
    ----------
    guild_badge : ``GuildBadge``
        The guild badge to check.
    """
    vampytest.assert_instance(guild_badge, GuildBadge)
    vampytest.assert_instance(guild_badge.enabled, bool)
    vampytest.assert_instance(guild_badge.guild_id, int)
    vampytest.assert_instance(guild_badge.icon, Icon)
    vampytest.assert_instance(guild_badge.tag, str)


def test__GuildBadge__new__no_fields():
    """
    Tests whether ``GuildBadge.__new__`` works as intended.
    
    Case: No fields given.
    """
    guild_badge = GuildBadge()
    _assert_fields_set(guild_badge)


def test__GuildBadge__new__all_fields():
    """
    Tests whether ``GuildBadge.__new__`` works as intended.
    
    Case: All fields given.
    """
    enabled = False
    guild_id = 202405170003
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    guild_badge = GuildBadge(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    _assert_fields_set(guild_badge)
    
    vampytest.assert_eq(guild_badge.enabled, enabled)
    vampytest.assert_eq(guild_badge.guild_id, guild_id)
    vampytest.assert_eq(guild_badge.icon, icon)
    vampytest.assert_eq(guild_badge.tag, tag)
