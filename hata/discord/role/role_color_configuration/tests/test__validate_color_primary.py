import vampytest

from ....color import Color

from ..fields import validate_color_primary


def _iter_options__passing():
    color = Color.from_rgb(33, 128, 1)
    
    yield None, Color(0)
    yield int(color), color
    yield color, color


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_color_primary(input_value):
    """
    Tests whether `validate_color_primary` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``Color``
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_color_primary(input_value)
    vampytest.assert_instance(output, Color)
    return output
