import vampytest

from ..fields import validate_author_types
from ..preinstanced import MessageSearchAuthorType


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
        MessageSearchAuthorType.bot,
        (
            MessageSearchAuthorType.bot,
        ),
    )
    
    yield (
        MessageSearchAuthorType.bot.value,
        (
            MessageSearchAuthorType.bot,
        ),
    )
    
    yield (
        [
            MessageSearchAuthorType.bot,
        ],
        (
            MessageSearchAuthorType.bot,
        ),
    )
    
    yield (
        [
            MessageSearchAuthorType.bot.value,
        ],
        (
            MessageSearchAuthorType.bot,
        ),
    )
    
    yield (
        [
            MessageSearchAuthorType.user,
            MessageSearchAuthorType.bot,
        ],
        (
            MessageSearchAuthorType.bot,
            MessageSearchAuthorType.user,
        ),
    )
    
    yield (
        [
            MessageSearchAuthorType.bot,
            MessageSearchAuthorType.user,
        ],
        (
            MessageSearchAuthorType.bot,
            MessageSearchAuthorType.user,
        ),
    )


def _iter_options__type_error():
    yield 12.6
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_author_types(input_value):
    """
    Tests whether `validate_author_types` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output :  ``None | tuple<MessageSearchAuthorType>``
    
    Raises
    ------
    TypeError
    """
    output = validate_author_types(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, MessageSearchAuthorType)
    
    return output
