import vampytest

from ....color import Color

from ..fields import validate_color


def _iter_options__passing():
    color = Color.from_rgb(33, 128, 1)
    
    yield None, None
    yield int(color), color
    yield color, color


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_color(input_value):
    """
    Tests whether `validate_color` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | Color``
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_color(input_value)
    vampytest.assert_instance(output, Color, nullable = True)
    return output
