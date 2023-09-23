import vampytest

from ..guild_inventory_settings import GuildInventorySettings


def _assert_fields_set(guild_inventory_settings):
    """
    Asserts whether every fields are set of the guild guild inventory settings.
    
    Parameters
    ----------
    guild_inventory_settings : ``GuildInventorySettings`
        The guild inventory settings to check.
    """
    vampytest.assert_instance(guild_inventory_settings, GuildInventorySettings)
    vampytest.assert_instance(guild_inventory_settings.emoji_pack_collectible, bool)
    vampytest.assert_instance(guild_inventory_settings.emoji_pack_collectible, bool)


def test__GuildInventorySettings__new__no_fields():
    """
    Tests whether ``GuildInventorySettings.__new__`` works as intended.
    
    Case: No fields given.
    """
    guild_inventory_settings = GuildInventorySettings()
    _assert_fields_set(guild_inventory_settings)


def test__GuildInventorySettings__new__all_fields():
    """
    Tests whether ``GuildInventorySettings.__new__`` works as intended.
    
    Case: All fields given.
    """
    emoji_pack_collectible = True
    
    guild_inventory_settings = GuildInventorySettings(
        emoji_pack_collectible = emoji_pack_collectible,
    )
    _assert_fields_set(guild_inventory_settings)
    
    vampytest.assert_eq(guild_inventory_settings.emoji_pack_collectible, emoji_pack_collectible)
