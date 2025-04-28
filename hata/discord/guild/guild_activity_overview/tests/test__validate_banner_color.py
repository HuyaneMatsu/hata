import vampytest

from ....color import Color

from ..fields import validate_banner_color


def _iter_options__passing():
    color = Color.from_rgb(33, 128, 1)
    
    yield None, None
    yield int(color), color
    yield color, color


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield -1
    yield 999999999


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_banner_color(input_value):
    """
    Tests whether `validate_banner_color` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | Color`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_banner_color(input_value)
