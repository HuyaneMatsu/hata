import vampytest

from ..fields import put_premium


def _iter_options():
    yield False, False, {}
    yield False, True, {'premium': False}
    yield True, False, {'premium': True}
    yield True, True, {'premium': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_premium(input_value, defaults):
    """
    Tests whether ``put_premium`` works as intended.
    
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
    return put_premium(input_value, {}, defaults)
