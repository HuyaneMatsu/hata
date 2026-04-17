import vampytest

from ....color import Color

from ..fields import put_colors


def _iter_options():
    color_0 = Color(1233)
    color_1 = Color(1236)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'colors': [],
        },
    )
    
    yield (
        (
            color_0,
            color_1,
        ),
        False,
        {
            'colors': [
                format(color_0, 'X'),
                format(color_1, 'X')
            ],
        },
    )
    
    yield (
        (
            color_0,
            color_1,
        ),
        True,
        {
            'colors': [
                format(color_0, 'X'),
                format(color_1, 'X')
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_colors(input_value, defaults):
    """
    Tests whether ``put_colors`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<Color>``
        Value to serialize.
    
    defaults : `bool`
        Whether values as their default should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_colors(input_value, {}, defaults)
