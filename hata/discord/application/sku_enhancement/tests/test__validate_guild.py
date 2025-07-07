import vampytest

from ...sku_enhancement_guild import SKUEnhancementGuild

from ..fields import validate_guild


def _iter_options__passing():
    sku_enhancement_guild = SKUEnhancementGuild(
        additional_emoji_slots = 50,
    )
    
    yield None, None
    yield sku_enhancement_guild, sku_enhancement_guild


def _iter_options__type_error():
    yield 12.6
    yield '12'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_guild(input_value):
    """
    Tests whether `validate_guild` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : ``None | SKUEnhancementGuild`˛
    
    Raises
    ------
    TypeError
    """
    output = validate_guild(input_value)
    vampytest.assert_instance(output, SKUEnhancementGuild, nullable = True)
    return output
