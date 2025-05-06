import vampytest

from ..fields import put_duration


def _iter_options():
    yield 0, False, {'duration_seconds': 0}
    yield 0, True, {'duration_seconds': 0}
    yield 60, False, {'duration_seconds': 60}
    yield 60, True, {'duration_seconds': 60}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_duration(input_value, defaults):
    """
    Tests whether ``put_duration`` is working as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_duration(input_value, {}, defaults)
