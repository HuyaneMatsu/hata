import vampytest

from ..fields import validate_revoked


def _iter_options():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_revoked__passing(input_value):
    """
    Tests whether `validate_revoked` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    validates
    """
    return validate_revoked(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_revoked__type_error(input_value):
    """
    Tests whether `validate_revoked` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_revoked(input_value)
