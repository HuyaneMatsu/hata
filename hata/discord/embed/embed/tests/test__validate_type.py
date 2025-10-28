import vampytest

from ..fields import validate_type
from ..preinstanced import EmbedType


def _iter_options__passing():
    yield (
        None,
        EmbedType.rich,
    )
    
    yield (
        EmbedType.gifv,
        EmbedType.gifv,
    )
    
    yield (
        EmbedType.gifv.value,
        EmbedType.gifv,
    )


def _iter_option__type_error():
    yield 12.6
    yield 0


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_option__type_error()).raising(TypeError))
def test__validate_type(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``EmbedType``
    
    Raises
    ------
    TypeError
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, EmbedType)
    return output
