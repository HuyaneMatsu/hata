import vampytest

from ....color import Color

from ..fields import put_badge_color_primary


def _iter_options():
    color = Color.from_rgb(33, 128, 1)
    
    yield (
        None,
        False,
        {
            'badge_color_primary': None,
        },
    )
    
    yield (
        None,
        True,
        {
            'badge_color_primary': None,
        },
    )
    
    yield (
        color,
        False,
        {
            'badge_color_primary': color.as_html,
        },
    )
    
    yield (
        color,
        True,
        {
            'badge_color_primary': color.as_html,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_badge_color_primary(input_value, defaults):
    """
    Tests whether ``put_badge_color_primary`` works as intended.
    
    Parameters
    ----------
    banner_color : `None | Color`
        Value to serialize.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<int, object>`
    """
    return put_badge_color_primary(input_value, {}, defaults)
