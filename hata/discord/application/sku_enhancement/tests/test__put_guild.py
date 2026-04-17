import vampytest

from ...sku_enhancement_guild import SKUEnhancementGuild

from ..fields import put_guild


def _iter_options():
    sku_enhancement_guild = SKUEnhancementGuild(
        additional_emoji_slots = 50,
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'guild_features': None,
        },
    )
    
    yield (
        sku_enhancement_guild,
        False,
        {
            'guild_features': sku_enhancement_guild.to_data(defaults = False)
        },
    )
    
    yield (
        sku_enhancement_guild,
        True,
        {
            'guild_features': sku_enhancement_guild.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild(input_value, defaults):
    """
    Tests whether ``put_guild`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | SKUEnhancementGuild``
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_guild(input_value, {}, defaults)
