import vampytest

from ....color import Color

from ..fields import put_banner_color


def _iter_options():
    color = Color.from_rgb(33, 128, 1)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'accent_color': None,
        },
    )
    
    yield (
        color,
        False,
        {
            'accent_color': int(color),
        },
    )
    
    yield (
        color,
        True,
        {
            'accent_color': int(color),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_banner_color(input_value, defaults):
    """
    Tests whether ``put_banner_color`` works as intended.
    
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
    return put_banner_color(input_value, {}, defaults)
