import vampytest

from ....embed import EmbedType

from ..fields import validate_embed_types


def _iter_options__passing():
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        EmbedType.gift,
        (
            EmbedType.gift,
        ),
    )
    
    yield (
        EmbedType.gift.value,
        (
            EmbedType.gift,
        ),
    )
    
    yield (
        [
            EmbedType.gift,
        ],
        (
            EmbedType.gift,
        ),
    )
    
    yield (
        [
            EmbedType.gift.value,
        ],
        (
            EmbedType.gift,
        ),
    )
    
    yield (
        [
            EmbedType.rich,
            EmbedType.gift,
        ],
        (
            EmbedType.gift,
            EmbedType.rich,
        ),
    )
    
    yield (
        [
            EmbedType.gift,
            EmbedType.rich,
        ],
        (
            EmbedType.gift,
            EmbedType.rich,
        ),
    )


def _iter_options__type_error():
    yield 12.6
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_embed_types(input_value):
    """
    Tests whether `validate_embed_types` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output :  ``None | tuple<EmbedType>``
    
    Raises
    ------
    TypeError
    """
    output = validate_embed_types(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, EmbedType)
    
    return output
