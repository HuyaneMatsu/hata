import vampytest

from ..fields import put_occurrence_count_limit


def _iter_options():
    yield 0, False, {}
    yield 0, True, {'count': 0}
    yield 1, False, {'count': 1}
    yield 1, True, {'count': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_occurrence_count_limit(input_value, defaults):
    """
    Tests whether ``put_occurrence_count_limit`` works as intended.
    
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
    return put_occurrence_count_limit(input_value, {}, defaults)
