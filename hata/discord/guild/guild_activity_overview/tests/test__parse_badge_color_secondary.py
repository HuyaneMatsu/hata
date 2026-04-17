import vampytest

from ....color import Color

from ..fields import parse_badge_color_secondary


def _iter_options():
    color = Color.from_rgb(33, 128, 1)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'badge_color_secondary': None,
        },
        None,
    )
    
    yield (
        {
            'badge_color_secondary': color.as_html,
        },
        color,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_badge_color_secondary(input_data):
    """
    Tests whether ``parse_badge_color_secondary`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | Color`
    """
    output = parse_badge_color_secondary(input_data)
    vampytest.assert_instance(output, Color, nullable = True)
    return output
