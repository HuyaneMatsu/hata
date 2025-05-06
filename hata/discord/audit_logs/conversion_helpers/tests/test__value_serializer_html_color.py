import vampytest

from ....color import Color

from ..converters import value_serializer_html_color


def _iter_options():
    color = Color.from_rgb(5, 6, 8)
    
    yield None, None
    yield color, color.as_html


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_serializer_html_color(input_value):
    """
    Tests whether ``value_serializer_html_color`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Color`
        Processed value.
    
    Returns
    -------
    output : `None | str`
    """
    output = value_serializer_html_color(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
