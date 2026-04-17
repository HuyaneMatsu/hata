import vampytest

from ..fields import put_consumed


def _iter_options():
    yield False, False, {}
    yield False, True, {'consumed': False}
    yield True, False, {'consumed': True}
    yield True, True, {'consumed': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_consumed(input_value, defaults):
    """
    Tests whether ``put_consumed`` works as intended.
    
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
    return put_consumed(input_value, {}, defaults)
