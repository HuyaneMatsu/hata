import vampytest

from ..fields import put_mention_limit


def _iter_options():
    yield 0, False, {'mention_total_limit': 0}
    yield 0, True, {'mention_total_limit': 0}
    yield 1, False, {'mention_total_limit': 1}
    yield 1, True, {'mention_total_limit': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mention_limit(input_value, defaults):
    """
    Tests whether ``put_mention_limit`` works as intended.
    
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
    return put_mention_limit(input_value, {}, defaults)
