import vampytest

from ..guild_inventory_settings import GuildInventorySettings

from .test__GuildInventorySettings__constructor import _assert_fields_set


def test__GuildInventorySettings__from_data():
    """
    Tests whether ``GuildInventorySettings.from_data`` works as intended.
    
    Case: All fields given.
    """
    emoji_pack_collectible = True
    
    data = {
        'is_emoji_pack_collectible': emoji_pack_collectible,
    }
    
    guild_inventory_settings = GuildInventorySettings.from_data(data)
    _assert_fields_set(guild_inventory_settings)
    
    vampytest.assert_eq(guild_inventory_settings.emoji_pack_collectible, emoji_pack_collectible)


def test__GuildInventorySettings__to_data():
    """
    Tests whether ``GuildInventorySettings.to_data`` works as intended.
    
    Case: Include defaults.
    """
    emoji_pack_collectible = True
    
    guild_inventory_settings = GuildInventorySettings(
        emoji_pack_collectible = emoji_pack_collectible,
    )
    
    expected_output = {
        'is_emoji_pack_collectible': emoji_pack_collectible,
    }
    
    vampytest.assert_eq(
        guild_inventory_settings.to_data(defaults = True),
        expected_output,
    )
