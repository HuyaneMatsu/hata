import vampytest

from ...guild_inventory_settings import GuildInventorySettings

from ..fields import validate_inventory_settings


def _iter_options():
    yield None, None
    
    inventory_settings = GuildInventorySettings(emoji_pack_collectible = True)
    
    yield inventory_settings, inventory_settings


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_inventory_settings__passing(input_value):
    """
    Tests whether ``validate_inventory_settings`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | GuildInventorySettings`
    """
    return validate_inventory_settings(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with('aya')
def test__validate_inventory_settings__type_error(input_value):
    """
    Tests whether ``validate_inventory_settings`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    return validate_inventory_settings(input_value)
