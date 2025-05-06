import vampytest

from ..fields import put_enabled


def _iter_options():
    yield False, False, {'disabled': True}
    yield True, False, {}
    yield False, True, {'disabled': True}
    yield True, True, {'disabled': False}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_enabled(input_value, defaults):
    """
    Tests whether ``put_enabled`` is working as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to serialize.
    
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    """
    return put_enabled(input_value, {}, defaults)
