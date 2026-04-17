import vampytest

from ....color import Color

from ..converters import value_deserializer_html_color


def _iter_options():
    color = Color.from_rgb(5, 6, 8)
    
    yield None, None
    yield color.as_html, color


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_deserializer_html_color(input_value):
    """
    Tests whether ``value_deserializer_html_color`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | Color`
    """
    output = value_deserializer_html_color(input_value)
    vampytest.assert_instance(output, Color, nullable = True)
    return output
