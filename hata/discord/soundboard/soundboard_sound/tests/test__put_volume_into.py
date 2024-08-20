import vampytest

from ..fields import put_volume_into


def _iter_options():
    yield 0.0, False, {'volume': 0.0}
    yield 0.0, True, {'volume': 0.0}
    yield 1.0, False, {}
    yield 1.0, True, {'volume': 1.0}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_volume_into(input_value, defaults):
    """
    Tests whether ``put_volume_into`` works as intended.
    
    Parameters
    ----------
    input_value : `float`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_volume_into(input_value, {}, defaults)
