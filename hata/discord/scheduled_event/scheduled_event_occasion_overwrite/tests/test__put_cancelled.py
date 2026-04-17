
import vampytest

from ..fields import put_cancelled


def _iter_options():
    yield False, False, {'is_canceled': False}
    yield False, True, {'is_canceled': False}
    yield True, False, {'is_canceled': True}
    yield True, True, {'is_canceled': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_cancelled(input_value, defaults):
    """
    Tests whether ``put_cancelled`` works as intended.
    
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
    return put_cancelled(input_value, {}, defaults)
