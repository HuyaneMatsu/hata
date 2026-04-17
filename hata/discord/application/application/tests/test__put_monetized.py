import vampytest

from ..fields import put_monetized


def _iter_options():
    yield False, False, {}
    yield False, True, {'is_monetized': False}
    yield True, False, {'is_monetized': True}
    yield True, True, {'is_monetized': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_monetized(input_value, defaults):
    """
    Tests whether ``put_monetized`` works as intended.
    
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
    return put_monetized(input_value, {}, defaults)
