
import vampytest

from ..fields import put_spoiler


def _iter_options():
    yield (
        False,
        False,
        {},
    )
    
    yield (
        False,
        True,
        {
            'is_spoiler': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'is_spoiler': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'is_spoiler': True,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_spoiler(input_value, defaults):
    """
    Tests whether ``put_spoiler`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_spoiler(input_value, {}, defaults)
