import vampytest

from ..fields import validate_mfa_enabled


def _iter_options__passing():
    yield None, False
    yield False, False
    yield True, True


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_mfa_enabled(input_value):
    """
    Tests whether `validate_mfa_enabled` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `bool`
    
    Raising
    -------
    TypeError
    """
    return validate_mfa_enabled(input_value)
