import vampytest

from ..fields import validate_emojis_enabled


def _iter_options():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_emojis_enabled__passing(input_value):
    """
    Tests whether `validate_emojis_enabled` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    validates
    """
    return validate_emojis_enabled(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_emojis_enabled__type_error(input_value):
    """
    Tests whether `validate_emojis_enabled` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_emojis_enabled(input_value)
