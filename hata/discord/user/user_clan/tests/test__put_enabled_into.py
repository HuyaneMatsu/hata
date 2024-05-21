import vampytest

from ..fields import put_enabled_into


def _iter_options():
    yield False, False, {'identity_enabled': False}
    yield True, False, {'identity_enabled': True}
    yield False, True, {'identity_enabled': False}
    yield True, True, {'identity_enabled': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_enabled_into(input_value, defaults):
    """
    Tests whether ``put_enabled_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to serialize.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    """
    return put_enabled_into(input_value, {}, defaults)
