import vampytest

from ..fields import validate_mfa_level
from ..preinstanced import MfaLevel


def _iter_options__passing():
    yield None, MfaLevel.none
    yield MfaLevel.elevated, MfaLevel.elevated
    yield MfaLevel.elevated.value, MfaLevel.elevated


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_mfa_level(input_value):
    """
    Tests whether `validate_mfa_level` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``MfaLevel``
    
    Raises
    ------
    TypeError
    """
    output = validate_mfa_level(input_value)
    vampytest.assert_instance(output, MfaLevel)
    return output
