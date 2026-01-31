import vampytest

from ..fields import validate_has_types
from ..preinstanced import MessageSearchHasType


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
        MessageSearchHasType.embed,
        (
            MessageSearchHasType.embed,
        ),
    )
    
    yield (
        MessageSearchHasType.embed.value,
        (
            MessageSearchHasType.embed,
        ),
    )
    
    yield (
        [
            MessageSearchHasType.embed,
        ],
        (
            MessageSearchHasType.embed,
        ),
    )
    
    yield (
        [
            MessageSearchHasType.embed.value,
        ],
        (
            MessageSearchHasType.embed,
        ),
    )
    
    yield (
        [
            MessageSearchHasType.image,
            MessageSearchHasType.embed,
        ],
        (
            MessageSearchHasType.embed,
            MessageSearchHasType.image,
        ),
    )
    
    yield (
        [
            MessageSearchHasType.embed,
            MessageSearchHasType.image,
        ],
        (
            MessageSearchHasType.embed,
            MessageSearchHasType.image,
        ),
    )


def _iter_options__type_error():
    yield 12.6
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_has_types(input_value):
    """
    Tests whether `validate_has_types` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output :  ``None | tuple<MessageSearchHasType>``
    
    Raises
    ------
    TypeError
    """
    output = validate_has_types(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, MessageSearchHasType)
    
    return output
