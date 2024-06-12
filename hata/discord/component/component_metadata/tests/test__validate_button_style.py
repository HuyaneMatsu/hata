import vampytest

from ..fields import validate_button_style
from ..preinstanced import ButtonStyle


def _iter_options__passing():
    yield ButtonStyle.link, ButtonStyle.link
    yield ButtonStyle.link.value, ButtonStyle.link
    yield None, ButtonStyle.none


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_button_style(input_value):
    """
    Tests whether `validate_button_style` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to validate.
    
    Returns
    -------
    output : ``ButtonStyle``
    
    Raises
    ------
    TypeError
    """
    output = validate_button_style(input_value)
    vampytest.assert_instance(output, ButtonStyle)
    return output
