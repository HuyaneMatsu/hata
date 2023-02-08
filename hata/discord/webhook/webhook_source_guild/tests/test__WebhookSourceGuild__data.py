import vampytest

from ....bases import Icon, IconType
from ..guild import WebhookSourceGuild

from .test__WebhookSourceGuild__constructor import _assert_fields_set


def test__WebhookSourceGuild__from_data():
    """
    Tests whether ``WebhookSourceGuild.from_data`` works as intended.
    """
    guild_id = 202302010014
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    data = {
        'id': str(guild_id),
        'icon': icon.as_base_16_hash,
        'name': name,
    }
    
    guild = WebhookSourceGuild.from_data(data)
    _assert_fields_set(guild)
    
    vampytest.assert_eq(guild.id, guild_id)
    vampytest.assert_eq(guild.icon, icon)
    vampytest.assert_eq(guild.name, name)


def test__WebhookSourceGuild__to_data():
    """
    Tests whether ``WebhookSourceGuild.to_data`` works as intended.
    
    Case: Include defaults.
    """
    guild_id = 202302010015
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    guild = WebhookSourceGuild(
        guild_id = guild_id,
        icon = icon,
        name = name,
    )
    
    expected_output = {
        'id': str(guild_id),
        'icon': icon.as_base_16_hash,
        'name': name,
    }
    
    vampytest.assert_eq(
        guild.to_data(defaults = True),
        expected_output,
    )
