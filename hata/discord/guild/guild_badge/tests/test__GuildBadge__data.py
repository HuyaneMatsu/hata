import vampytest

from ....bases import Icon, IconType

from ..guild_badge import GuildBadge

from .test__GuildBadge__constructor import _assert_fields_set


def test__GuildBadge__from_data():
    """
    Tests whether ``GuildBadge.from_data`` works as intended.
    """
    enabled = False 
    guild_id = 202405170004
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    data = {
        'identity_enabled': enabled,
        'identity_guild_id': str(guild_id),
        'badge': icon.as_base_16_hash,
        'tag': tag,
    }
    
    guild_badge = GuildBadge.from_data(data)
    _assert_fields_set(guild_badge)
    
    vampytest.assert_eq(guild_badge.enabled, enabled)
    vampytest.assert_eq(guild_badge.guild_id, guild_id)
    vampytest.assert_eq(guild_badge.icon, icon)
    vampytest.assert_eq(guild_badge.tag, tag)


def test__GuildBadge__to_data():
    """
    Tests whether ``GuildBadge.to_data`` works as intended.
    
    Case: Include defaults.
    """
    enabled = False
    guild_id = 202405170005
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    guild_badge = GuildBadge(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    
    expected_output = {
        'identity_enabled': enabled,
        'identity_guild_id': str(guild_id),
        'badge': icon.as_base_16_hash,
        'tag': tag,
    }
    
    vampytest.assert_eq(
        guild_badge.to_data(defaults = True),
        expected_output,
    )
