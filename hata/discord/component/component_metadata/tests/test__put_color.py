import vampytest

from ....color import Color

from ..fields import put_color


def _iter_options():
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
        Color(0),
        False,
        {
            'accent_color': 0,
        },
    )
    
    yield (
        Color(0),
        True,
        {
            'accent_color': 0,
        },
    )
    
    yield (
        Color(1),
        False,
        {
            'accent_color': 1,
        },
    )
    
    yield (
        Color(1),
        True,
        {
            'accent_color': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_color(input_value, defaults):
    """
    Tests whether ``put_color`` is working as intended.
    
    Parameters
    ----------
    value : ``None | Color``
        Value to serialize.
    
    defaults : `bool`
        Whether to include values as their default.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_color(input_value, {}, defaults)
