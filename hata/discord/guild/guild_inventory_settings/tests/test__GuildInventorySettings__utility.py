import vampytest

from ..guild_inventory_settings import GuildInventorySettings

from .test__GuildInventorySettings__constructor import _assert_fields_set


def test__GuildInventorySettings__copy():
    """
    Tests whether ``GuildInventorySettings.copy`` works as intended.
    """
    emoji_pack_collectible = True
    
    guild_inventory_settings = GuildInventorySettings(
        emoji_pack_collectible = emoji_pack_collectible,
    )
    
    copy = guild_inventory_settings.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_inventory_settings)
    
    vampytest.assert_eq(copy, guild_inventory_settings)


def test__GuildInventorySettings__copy_with__no_fields():
    """
    Tests whether ``GuildInventorySettings.copy_with`` works as intended.
    
    Case: No fields given.
    """
    emoji_pack_collectible = True
    
    guild_inventory_settings = GuildInventorySettings(
        emoji_pack_collectible = emoji_pack_collectible,
    )
    
    copy = guild_inventory_settings.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_inventory_settings)
    
    vampytest.assert_eq(copy, guild_inventory_settings)


def test__GuildInventorySettings__copy_with_all_fields1():
    """
    Tests whether ``GuildInventorySettings.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_emoji_pack_collectible = True
    
    new_emoji_pack_collectible = False
    
    guild_inventory_settings = GuildInventorySettings(
        emoji_pack_collectible = old_emoji_pack_collectible,
    )
    
    copy = guild_inventory_settings.copy_with(
        emoji_pack_collectible = new_emoji_pack_collectible,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_inventory_settings)
    
    vampytest.assert_eq(copy.emoji_pack_collectible, new_emoji_pack_collectible)
