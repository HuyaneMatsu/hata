import vampytest

from ..constants import NONCE_LENGTH_MAX
from ..fields import validate_nonce


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'a', 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_nonce__passing(nonce):
    """
    Tests whether `validate_nonce` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    nonce : `None | str`
        Nonce to validate.
    
    Returns
    -------
    output : `None | str`
    """
    return validate_nonce(nonce)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_nonce__type_error(nonce):
    """
    Tests whether `validate_nonce` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    nonce : `None | str`
        Nonce to validate with.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_nonce(nonce)


@vampytest.raising(ValueError)
@vampytest.call_with('a' * (NONCE_LENGTH_MAX + 1))
def test__validate_nonce__value_error(nonce):
    """
    Tests whether `validate_nonce` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    nonce : `None | str`
        Nonce to validate with.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_nonce(nonce)
