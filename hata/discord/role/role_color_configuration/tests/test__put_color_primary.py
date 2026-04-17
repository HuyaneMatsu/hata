
import vampytest

from ....color import Color

from ..fields import put_color_primary


def _iter_options():
    yield (
        Color(0),
        False,
        {},
    )
    
    yield (
        Color(0),
        True,
        {
            'primary_color': 0,
        },
    )
    
    yield (
        Color(1),
        False,
        {
            'primary_color': 1,
        },
    )
    
    yield (
        Color(1),
        True,
        {
            'primary_color': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_color_primary(input_value, defaults):
    """
    Tests whether ``put_color_primary`` is working as intended.
    
    Parameters
    ----------
    value : ``Color``
        Value to serialize.
    
    defaults : `bool`
        Whether to include values as their default.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_color_primary(input_value, {}, defaults)
