import vampytest

from ...guild_inventory_settings import GuildInventorySettings

from ..fields import put_inventory_settings


def _iter_options():
    yield None, False, {'inventory_settings': None}
    yield None, True, {'inventory_settings': None}
    
    inventory_settings = GuildInventorySettings(emoji_pack_collectible = True)
    
    yield inventory_settings, False, {'inventory_settings': inventory_settings.to_data(defaults = False)}
    yield inventory_settings, True, {'inventory_settings': inventory_settings.to_data(defaults = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_inventory_settings(input_value, defaults):
    """
    Tests whether ``put_inventory_settings`` works as intended.
    
    Parameters
    ----------
    input_value : `None | GuildInventorySettings`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_inventory_settings(input_value, {}, defaults)
