
import vampytest

from ....color import Color

from ..fields import put_color_tertiary


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
            'tertiary_color': None,
        },
    )
    
    yield (
        Color(1),
        False,
        {
            'tertiary_color': 1,
        },
    )
    
    yield (
        Color(1),
        True,
        {
            'tertiary_color': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_color_tertiary(input_value, defaults):
    """
    Tests whether ``put_color_tertiary`` is working as intended.
    
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
    return put_color_tertiary(input_value, {}, defaults)
