import vampytest

from ..fields import put_mfa_level
from ..preinstanced import MfaLevel


def _iter_options():
    yield MfaLevel.elevated, False, {'mfa_level': MfaLevel.elevated.value}
    yield MfaLevel.elevated, True, {'mfa_level': MfaLevel.elevated.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mfa_level(input_value, defaults):
    """
    Tests whether ``put_mfa_level`` works as intended.
    
    Parameters
    ----------
    input_value : ``MfaLevel``
        Value to serialize.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_mfa_level(input_value, {}, defaults)
