import vampytest

from ...guild_inventory_settings import GuildInventorySettings

from ..fields import parse_inventory_settings


def _iter_options():
    yield {}, None
    yield {'inventory_settings': None}, None
    yield {'inventory_settings': {}}, GuildInventorySettings()
    yield (
        {'inventory_settings': {'is_emoji_pack_collectible': True}},
        GuildInventorySettings(emoji_pack_collectible = True),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_inventory_settings(input_data):
    """
    Tests whether ``parse_inventory_settings`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | GuildInventorySettings`
    """
    return parse_inventory_settings(input_data)
