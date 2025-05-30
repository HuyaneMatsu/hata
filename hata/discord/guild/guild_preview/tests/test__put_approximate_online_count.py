import vampytest

from ..fields import put_approximate_online_count


def _iter_options():
    yield 0, False, {'approximate_presence_count': 0}
    yield 0, True, {'approximate_presence_count': 0}
    yield 1, False, {'approximate_presence_count': 1}
    yield 1, True, {'approximate_presence_count': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_approximate_online_count(input_value, defaults):
    """
    Tests whether ``put_approximate_online_count`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_approximate_online_count(input_value, {}, defaults)
