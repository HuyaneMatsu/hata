import vampytest

from ..guild_inventory_settings import GuildInventorySettings


def test__GuildInventorySettings__repr():
    """
    Tests whether ``GuildInventorySettings.__repr__`` works as intended.
    """
    emoji_pack_collectible = True
    
    guild_inventory_settings = GuildInventorySettings(
        emoji_pack_collectible = emoji_pack_collectible,
    )
    
    vampytest.assert_instance(repr(guild_inventory_settings), str)


def test__GuildInventorySettings__hash():
    """
    Tests whether ``GuildInventorySettings.__hash__`` works as intended.
    """
    emoji_pack_collectible = True
    
    guild_inventory_settings = GuildInventorySettings(
        emoji_pack_collectible = emoji_pack_collectible,
    )
    
    vampytest.assert_instance(hash(guild_inventory_settings), int)


def test__GuildInventorySettings__eq():
    """
    Tests whether ``GuildInventorySettings.__eq__`` works as intended.
    """
    emoji_pack_collectible = True
    
    keyword_parameters = {
        'emoji_pack_collectible': emoji_pack_collectible,
    }
    
    guild_inventory_settings = GuildInventorySettings(**keyword_parameters)
    
    vampytest.assert_eq(guild_inventory_settings, guild_inventory_settings)
    vampytest.assert_ne(guild_inventory_settings, object())
    
    for field_name, field_value in (
        ('emoji_pack_collectible', False),
    ):
        test_guild_inventory_settings = GuildInventorySettings(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(guild_inventory_settings, test_guild_inventory_settings)


def _iter_options__bool():
    yield GuildInventorySettings(), False
    yield GuildInventorySettings(emoji_pack_collectible = True), True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__GuildInventorySettings__bool(guild_inventory_settings):
    """
    Tests whether ``GuildInventorySettings.__bool__`` works as intended.
    
    Parameters
    ----------
    guild_inventory_settings : ``GuildInventorySettings``
        The guild inventory setting to get its boolean value of.
    
    Returns
    -------
    output : `bool`
    """
    output = bool(guild_inventory_settings)
    vampytest.assert_instance(output, bool)
    return output
