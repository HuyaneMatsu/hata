import vampytest

from ....color import Color

from ..fields import validate_colors


def _iter_options__passing():
    color_0 = Color(1233)
    color_1 = Color(1236)
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            color_0,
            color_1,
        ],
        (
            color_0,
            color_1,
        ),
    )


def _iter_option__type_error():
    yield 'nyan'
    yield ['nyan']


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_option__type_error()).raising(TypeError))
def test__validate_colors(input_value):
    """
    Tests whether ``validate_colors`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``None | tuple<Color>``
    
    Raises
    ------
    TypeError
    """
    output = validate_colors(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Color)
    
    return output
