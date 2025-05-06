import vampytest

from ..fields import put_max_uses


def _iter_options():
    yield 0, False, {'max_uses': 0}
    yield 0, True, {'max_uses': 0}
    yield None, False, {}
    yield None, True, {'max_uses': None}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_max_uses(input_value, defaults):
    """
    Tests whether ``put_max_uses`` works as intended.
    
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
    return put_max_uses(input_value, {}, defaults)
