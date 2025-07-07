import vampytest

from ...sku_enhancement_guild import SKUEnhancementGuild

from ..fields import parse_guild


def _iter_options():
    sku_enhancement_guild = SKUEnhancementGuild(
        additional_emoji_slots = 50,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'guild_features': None,
        },
        None,
    )
    
    yield (
        {
            'guild_features': sku_enhancement_guild.to_data(),
        },
        sku_enhancement_guild,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_guild(input_data):
    """
    Tests whether ``parse_guild`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | SKUEnhancementGuild`˛
    """
    output = parse_guild(input_data)
    vampytest.assert_instance(output, SKUEnhancementGuild, nullable = True)
    return output
