import vampytest

from ....bases import Icon, IconType

from ..user_clan import UserClan

from .test__UserClan__constructor import _assert_fields_set


def test__UserClan__from_data():
    """
    Tests whether ``UserClan.from_data`` works as intended.
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
    
    user_clan = UserClan.from_data(data)
    _assert_fields_set(user_clan)
    
    vampytest.assert_eq(user_clan.enabled, enabled)
    vampytest.assert_eq(user_clan.guild_id, guild_id)
    vampytest.assert_eq(user_clan.icon, icon)
    vampytest.assert_eq(user_clan.tag, tag)


def test__UserClan__to_data():
    """
    Tests whether ``UserClan.to_data`` works as intended.
    
    Case: Include defaults.
    """
    enabled = False
    guild_id = 202405170005
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    user_clan = UserClan(
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
        user_clan.to_data(defaults = True),
        expected_output,
    )
