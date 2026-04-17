import vampytest

from ..fields import put_unique


def _iter_options():
    yield False, False, {}
    yield False, True, {'unique': False}
    yield True, False, {'unique': True}
    yield True, True, {'unique': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_unique(input_value, defaults):
    """
    Tests whether ``put_unique`` works as intended.
    
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
    return put_unique(input_value, {}, defaults)
