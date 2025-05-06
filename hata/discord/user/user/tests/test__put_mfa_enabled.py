import vampytest

from ..fields import put_mfa_enabled


def _iter_options():
    yield False, False, {}
    yield False, True, {'mfa_enabled': False}
    yield True, False, {'mfa_enabled': True}
    yield True, True, {'mfa_enabled': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mfa_enabled(input_value, defaults):
    """
    Tests whether ``put_mfa_enabled`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to serialize.
    defaults : `bool`
        Whether fields withe their value should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_mfa_enabled(input_value, {}, defaults)
