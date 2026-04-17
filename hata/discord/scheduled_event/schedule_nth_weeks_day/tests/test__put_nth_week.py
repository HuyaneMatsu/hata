import vampytest

from ..fields import put_nth_week


def _iter_options():
    yield 1, False, {'n': 1}
    yield 1, True, {'n': 1}
    yield 2, False, {'n': 2}
    yield 2, True, {'n': 2}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_nth_week(input_value, defaults):
    """
    Tests whether ``put_nth_week`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_nth_week(input_value, {}, defaults)
