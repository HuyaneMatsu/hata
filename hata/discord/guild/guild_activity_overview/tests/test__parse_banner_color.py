import vampytest

from ....color import Color

from ..fields import parse_banner_color


def _iter_options():
    color = Color.from_rgb(33, 128, 1)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'brand_color_primary': None,
        },
        None,
    )
    
    yield (
        {
            'brand_color_primary': color.as_html,
        },
        color,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_banner_color(input_data):
    """
    Tests whether ``parse_banner_color`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | Color`
    """
    output = parse_banner_color(input_data)
    vampytest.assert_instance(output, Color, nullable = True)
    return output
