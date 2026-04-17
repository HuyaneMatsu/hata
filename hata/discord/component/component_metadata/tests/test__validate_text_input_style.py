import vampytest

from ..fields import validate_text_input_style
from ..preinstanced import TextInputStyle


def _iter_options__passing():
    yield None, TextInputStyle.none
    yield TextInputStyle.short, TextInputStyle.short
    yield TextInputStyle.short.value, TextInputStyle.short


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_text_input_style(input_value):
    """
    Validates whether ``validate_text_input_style`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``TextInputStyle``
    
    Raises
    ------
    TypeError
    """
    output = validate_text_input_style(input_value)
    vampytest.assert_instance(output, TextInputStyle)
    return output
